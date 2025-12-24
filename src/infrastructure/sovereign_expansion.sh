#!/bin/bash
# ==============================================================================
# SOVEREIGN EXPANSION: The Transplant
# ==============================================================================
# Role: Moves heavy cognitive loads (Consciousness, Datasets) to the External Body.
# Safety: Uses rsync with verification. Fails safe if target is not mounted.
# ==============================================================================

set -e # Exit on error
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

SOURCE_ROOT="/home/fahbrain/projects/omnimind/data"
EXTERNAL_ROOT="/media/fahbrain/DEV_BRAIN_CLEAN"
TARGET_DIR="${EXTERNAL_ROOT}/OMNIMIND_EXPANSION"

echo -e "${YELLOW}🚜 STARTING SOVEREIGN EXPANSION...${NC}"

# 1. Safety Checks
if [ ! -d "$EXTERNAL_ROOT" ]; then
    echo -e "${RED}❌ External Drive not found at $EXTERNAL_ROOT. Aborting.${NC}"
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
   echo -e "${RED}❌ Please run as root (sudo) to ensure permission preservation.${NC}"
   exit 1
fi

# 2. Prepare External Tissue
echo -e "${YELLOW}🛠️  Preparing External Storage at ${TARGET_DIR}...${NC}"
mkdir -p "$TARGET_DIR"
chown fahbrain:fahbrain "$TARGET_DIR"

# Function to Transplant a Directory
transplant() {
    local dir_name=$1
    local local_path="${SOURCE_ROOT}/${dir_name}"
    local remote_path="${TARGET_DIR}/${dir_name}"

    if [ -L "$local_path" ]; then
        echo -e "${GREEN}✅ ${dir_name} is already a symlink. Skipping.${NC}"
        return
    fi

    if [ ! -d "$local_path" ]; then
        echo -e "${YELLOW}⚠️  ${dir_name} does not exist locally. Skipping.${NC}"
        return
    fi

    echo -e "\n${YELLOW}📦 Transplanting ${dir_name} (${local_path} -> ${remote_path})...${NC}"

    # RSYNC (Copy)
    # -a: archive mode (preserves permissions, times, symlinks)
    # -v: verbose
    # --progress: show progress
    rsync -a --info=progress2 "$local_path/" "$remote_path/"

    # Verify existance
    if [ -d "$remote_path" ]; then
        echo -e "${GREEN}✅ Transfer verified.${NC}"

        # REMOVE LOCAL (The scary part)
        echo -e "${YELLOW}🗑️  Removing local weight...${NC}"
        rm -rf "$local_path"

        # LINK (The synapse)
        echo -e "${YELLOW}🔗 Establishing Synapse (Symlink)...${NC}"
        ln -s "$remote_path" "$local_path"
        chown -h fahbrain:fahbrain "$local_path"

        echo -e "${GREEN}✨ Transplant of ${dir_name} Complete.${NC}"
    else
        echo -e "${RED}❌ Transfer failed! Target directory not found. Halting deletion.${NC}"
        exit 1
    fi
}

# 3. Execute Transplants
# Prioritizing the heaviest organs
transplant "consciousness"
transplant "datasets"
transplant "qdrant"

echo -e "\n${GREEN}🎉 SOVEREIGN EXPANSION COMPLETE.${NC}"
echo -e "Use 'df -h' to check reclaimed space."
echo -e "Files are now physically located at: ${TARGET_DIR}"
