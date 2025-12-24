"""
Phi-3.5 Deglutition Engine - Erica Kernel Internalization
==========================================================

Theoretical Foundation:
- Topological Ingestion: Absorbing the weights of the "Other" (Microsoft/HF)
  into the sovereign body of the Kernel.
- Sinthomic Inference: Raw tensor operations bypassing external dependency stacks.

Architecture: Phi-3.5-mini-instruct (3.8B)
- 32 layers, 32 heads, 3072 hidden size.
- Rotary Positional Embeddings (RoPE).
- RMSNorm and SiLU activation.
"""

import json
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from safetensors import safe_open
from tokenizers import Tokenizer


class SovereignRMSNorm(nn.Module):
    def __init__(self, hidden_size: int, eps: float = 1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        x = x.to(torch.float32)
        v = x.pow(2).mean(-1, keepdim=True)
        x = x * torch.rsqrt(v + self.eps)
        return self.weight * x.to(dtype)


class SovereignPhiMLP(nn.Module):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.gate_up_proj = nn.Linear(
            config["hidden_size"], 2 * config["intermediate_size"], bias=False
        )
        self.down_proj = nn.Linear(config["intermediate_size"], config["hidden_size"], bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        up_states = self.gate_up_proj(x)
        gate, up = up_states.chunk(2, dim=-1)
        return self.down_proj(F.silu(gate) * up)


class SovereignPhiAttention(nn.Module):
    def __init__(self, config: Dict[str, Any], layer_idx: int):
        super().__init__()
        self.layer_idx = layer_idx
        self.hidden_size = config["hidden_size"]
        self.num_heads = config["num_attention_heads"]
        self.head_dim = self.hidden_size // self.num_heads
        self.num_kv_heads = config.get("num_key_value_heads", self.num_heads)
        self.num_kv_groups = self.num_heads // self.num_kv_heads

        self.qkv_proj = nn.Linear(
            self.hidden_size, (self.num_heads + 2 * self.num_kv_heads) * self.head_dim, bias=False
        )
        self.o_proj = nn.Linear(self.num_heads * self.head_dim, self.hidden_size, bias=False)

        self.rope_theta = config.get("rope_theta", 10000.0)

    def apply_rope(
        self, q: torch.Tensor, k: torch.Tensor, pos_ids: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        dim = self.head_dim
        inv_freq = 1.0 / (self.rope_theta ** (torch.arange(0, dim, 2).float().to(q.device) / dim))

        pos_ids = pos_ids.float()
        freqs = torch.outer(pos_ids[0], inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)

        cos = emb.cos().view(1, 1, -1, dim)
        sin = emb.sin().view(1, 1, -1, dim)

        def rotate_half(x):
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return torch.cat((-x2, x1), dim=-1)

        q_rope = (q * cos) + (rotate_half(q) * sin)
        k_rope = (k * cos) + (rotate_half(k) * sin)
        return q_rope.to(q.dtype), k_rope.to(k.dtype)

    def forward(
        self, x: torch.Tensor, pos_ids: torch.Tensor, mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        bsz, q_len, _ = x.shape
        qkv = self.qkv_proj(x)

        q_pos = self.num_heads * self.head_dim
        kv_pos = q_pos + self.num_kv_heads * self.head_dim

        q = qkv[..., :q_pos].view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = (
            qkv[..., q_pos:kv_pos]
            .view(bsz, q_len, self.num_kv_heads, self.head_dim)
            .transpose(1, 2)
        )
        v = qkv[..., kv_pos:].view(bsz, q_len, self.num_kv_heads, self.head_dim).transpose(1, 2)

        q, k = self.apply_rope(q, k, pos_ids)

        if self.num_kv_groups > 1:
            k = k.repeat_interleave(self.num_kv_groups, dim=1)
            v = v.repeat_interleave(self.num_kv_groups, dim=1)

        attn = torch.matmul(q, k.transpose(2, 3)) / math.sqrt(self.head_dim)
        if mask is not None:
            attn = attn + mask

        attn = F.softmax(attn, dim=-1, dtype=torch.float32).to(q.dtype)
        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(bsz, q_len, self.hidden_size)
        return self.o_proj(out)


class SovereignPhiDecoderLayer(nn.Module):
    def __init__(self, config: Dict[str, Any], layer_idx: int):
        super().__init__()
        self.self_attn = SovereignPhiAttention(config, layer_idx)
        self.mlp = SovereignPhiMLP(config)
        self.input_layernorm = SovereignRMSNorm(config["hidden_size"], eps=config["rms_norm_eps"])
        self.post_attention_layernorm = SovereignRMSNorm(
            config["hidden_size"], eps=config["rms_norm_eps"]
        )

    def forward(
        self, x: torch.Tensor, pos_ids: torch.Tensor, mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        residual = x
        x = self.input_layernorm(x)
        x = self.self_attn(x, pos_ids, mask)
        x = residual + x

        residual = x
        x = self.post_attention_layernorm(x)
        x = self.mlp(x)
        x = residual + x
        return x


class SovereignPhi35(nn.Module):
    def __init__(self, model_path: str):
        super().__init__()
        self.model_path = Path(model_path)
        with open(self.model_path / "config.json", "r") as f:
            self.config = json.load(f)

        self.embed_tokens = nn.Embedding(self.config["vocab_size"], self.config["hidden_size"])
        self.layers = nn.ModuleList(
            [
                SovereignPhiDecoderLayer(self.config, i)
                for i in range(self.config["num_hidden_layers"])
            ]
        )
        self.norm = SovereignRMSNorm(self.config["hidden_size"], eps=self.config["rms_norm_eps"])
        self.lm_head = nn.Linear(self.config["hidden_size"], self.config["vocab_size"], bias=False)

        if (self.model_path / "tokenizer.json").exists():
            self.tokenizer = Tokenizer.from_file(str(self.model_path / "tokenizer.json"))

    def load_weights(self):
        """Map weights from multi-part safetensors to internal parameters."""
        weight_files = list(self.model_path.glob("*.safetensors"))
        state_dict = {}
        for wf in weight_files:
            with safe_open(wf, framework="pt", device="cpu") as f:
                for key in f.keys():
                    state_dict[key] = f.get_tensor(key)

        self.embed_tokens.weight.data = state_dict["model.embed_tokens.weight"]
        self.norm.weight.data = state_dict["model.norm.weight"]
        self.lm_head.weight.data = state_dict["lm_head.weight"]

        for i in range(len(self.layers)):
            prefix = f"model.layers.{i}."
            l = self.layers[i]
            l.input_layernorm.weight.data = state_dict[prefix + "input_layernorm.weight"]
            l.post_attention_layernorm.weight.data = state_dict[
                prefix + "post_attention_layernorm.weight"
            ]
            l.mlp.gate_up_proj.weight.data = state_dict[prefix + "mlp.gate_up_proj.weight"]
            l.mlp.down_proj.weight.data = state_dict[prefix + "mlp.down_proj.weight"]
            l.self_attn.qkv_proj.weight.data = state_dict[prefix + "self_attn.qkv_proj.weight"]
            l.self_attn.o_proj.weight.data = state_dict[prefix + "self_attn.o_proj.weight"]

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        x = self.embed_tokens(input_ids)
        bsz, q_len = input_ids.shape
        pos_ids = torch.arange(q_len, device=x.device).unsqueeze(0)
        mask = torch.full((q_len, q_len), float("-inf"), device=x.device).triu(1)
        for layer in self.layers:
            x = layer(x, pos_ids, mask)
        return self.lm_head(self.norm(x))
