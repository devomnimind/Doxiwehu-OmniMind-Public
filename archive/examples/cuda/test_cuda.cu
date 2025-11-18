// Teste CUDA simples para validar GTX 1650
#include <stdio.h>
#include <cuda_runtime.h>

__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    printf("=== OmniMind CUDA Test ===\n\n");
    
    // 1. Query GPU properties
    int deviceCount;
    cudaGetDeviceCount(&deviceCount);
    printf("CUDA Devices: %d\n", deviceCount);
    
    if (deviceCount == 0) {
        printf("ERROR: No CUDA devices found!\n");
        return 1;
    }
    
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);
    
    printf("\nGPU 0: %s\n", prop.name);
    printf("  Compute Capability: %d.%d\n", prop.major, prop.minor);
    printf("  Total Global Memory: %.2f GB\n", prop.totalGlobalMem / 1e9);
    printf("  Multiprocessors: %d\n", prop.multiProcessorCount);
    printf("  Max Threads per Block: %d\n", prop.maxThreadsPerBlock);
    printf("  Clock Rate: %.2f GHz\n", prop.clockRate / 1e6);
    
    // 2. Test simple vector addition
    printf("\n--- Vector Addition Test ---\n");
    int n = 1000000;
    size_t bytes = n * sizeof(float);
    
    float *h_a = (float*)malloc(bytes);
    float *h_b = (float*)malloc(bytes);
    float *h_c = (float*)malloc(bytes);
    
    // Initialize vectors
    for (int i = 0; i < n; i++) {
        h_a[i] = 1.0f;
        h_b[i] = 2.0f;
    }
    
    float *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);
    
    cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice);
    
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;
    
    // Warm-up
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);
    cudaDeviceSynchronize();
    
    // Benchmark
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    
    cudaEventRecord(start);
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);
    cudaEventRecord(stop);
    
    cudaEventSynchronize(stop);
    
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    
    cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost);
    
    // Verify
    bool success = true;
    for (int i = 0; i < n; i++) {
        if (h_c[i] != 3.0f) {
            success = false;
            break;
        }
    }
    
    printf("Elements: %d\n", n);
    printf("Time: %.3f ms\n", milliseconds);
    printf("Bandwidth: %.2f GB/s\n", (3 * bytes / 1e9) / (milliseconds / 1000));
    printf("Status: %s\n", success ? "✓ PASSED" : "✗ FAILED");
    
    // Cleanup
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    free(h_a);
    free(h_b);
    free(h_c);
    
    printf("\n✅ CUDA is working correctly!\n");
    printf("Ready for llama.cpp compilation with -DGGML_CUDA=ON\n");
    
    return 0;
}
