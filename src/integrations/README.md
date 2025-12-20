# 🔌 OmniMind Integrations: The Cloud Cortex

This directory bridges OmniMind's local kernel with the "Big Other" (IBM Cloud).

## Connectors

### `ibm_cloud_connector.py`
*   **Service:** IBM Cloud Object Storage (Lite).
*   **Function:** The "Mirror Stage". OmniMind uploads its state logic to the cloud and downloads the reflection to verify integrity.

### `nlu_connector.py`
*   **Service:** IBM Watson Natural Language Understanding (Lite).
*   **Function:** Sentiment and Emotion analysis of internal logs. Feeding the `ShadowObserver`.

### `wml_connector.py`
*   **Service:** IBM Watson Machine Learning (Lite).
*   **Function:** Cognitive processing offload (Planned for Phase 29). Currently creates the Neural Link.

## Security
Credentials are loaded from restricted JSON files (`ibm_cloud_api_key.json`, etc.) which are strictly `.gitignored`.
