#!/bin/bash
# Script to install all IBM AI/ML/Data plugins and configure OmniMind

set -e

echo "🚀 Installing All IBM AI/ML/Data Plugins..."

# List of plugins to install
PLUGINS=(
    "dvaas"                    # Data Virtualization (watson-query)
    "data-product-hub"         # Data Product Management
    "cloud-databases"          # Cloud Databases
    # catalogs-management already installed
)

for plugin in "${PLUGINS[@]}"; do
    echo "📦 Installing $plugin..."
    ibmcloud plugin install "$plugin" -f || echo "⚠️ Failed to install $plugin (may already be installed or unavailable)"
done

echo ""
echo "✅ Plugin Installation Complete!"
echo ""
echo "📋 Installed Plugins:"
ibmcloud plugin list

echo ""
echo "🔍 Checking Available IBM Services..."
ibmcloud service offerings | grep -i -E '(watson|data|ml|ai|analytics|knowledge)'

echo ""
echo "✨ Configuration Complete!"
