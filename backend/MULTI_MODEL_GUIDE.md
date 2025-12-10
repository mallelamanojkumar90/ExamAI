# Multi-Model LangChain Configuration Guide

## Overview

The ExamAI platform now supports multiple AI model providers through LangChain:

- **OpenAI**: GPT-4, GPT-4o, GPT-4o-mini, GPT-3.5-turbo
- **Google Gemini**: Gemini Pro, Gemini 1.5 Pro, Gemini 1.5 Flash
- **Anthropic Claude**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku

## Configuration

### 1. Environment Variables

Edit your `.env` file to add API keys:

```env
# OpenAI Configuration (already configured)
OPENAI_API_KEY=your_openai_api_key

# Google Gemini Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key

# Anthropic Claude Configuration
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key

# Default Model Configuration
DEFAULT_MODEL_PROVIDER=openai
DEFAULT_MODEL_NAME=gpt-4o-mini
DEFAULT_TEMPERATURE=0.7
```

### 2. Getting API Keys

#### OpenAI

- Already configured in your project
- Get keys from: https://platform.openai.com/api-keys

#### Google Gemini

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add to `.env`

#### Anthropic Claude

1. Visit: https://console.anthropic.com/
2. Sign up or sign in
3. Navigate to API Keys
4. Create a new key
5. Copy the key and add to `.env`

## API Usage

### List Available Models

```bash
GET http://localhost:8000/models
```

Response:

```json
{
  "models": {
    "openai": {
      "available": true,
      "api_key_configured": true,
      "models": [
        {
          "id": "gpt-4o-mini",
          "name": "GPT-4o Mini",
          "description": "Fast and cost-effective"
        },
        ...
      ]
    },
    "google": {
      "available": false,
      "api_key_configured": false,
      "models": [...]
    },
    "anthropic": {
      "available": false,
      "api_key_configured": false,
      "models": [...]
    }
  },
  "default": {
    "provider": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0.7
  }
}
```

### Generate Questions with Specific Model

```bash
POST http://localhost:8000/generate-questions
Content-Type: application/json

{
  "subject": "Physics",
  "difficulty": "medium",
  "count": 5,
  "exam_type": "IIT_JEE",
  "model_provider": "openai",
  "model_name": "gpt-4o-mini",
  "temperature": 0.7
}
```

### Using Default Model

If you don't specify model parameters, it will use the default configuration from `.env`:

```bash
POST http://localhost:8000/generate-questions
Content-Type: application/json

{
  "subject": "Physics",
  "difficulty": "medium",
  "count": 5,
  "exam_type": "IIT_JEE"
}
```

## Model Selection Guide

### OpenAI Models

| Model         | Speed  | Cost   | Quality    | Best For                        |
| ------------- | ------ | ------ | ---------- | ------------------------------- |
| gpt-4o-mini   | ⚡⚡⚡ | 💰     | ⭐⭐⭐     | General use, fast responses     |
| gpt-4o        | ⚡⚡   | 💰💰   | ⭐⭐⭐⭐   | Balanced performance            |
| gpt-4         | ⚡     | 💰💰💰 | ⭐⭐⭐⭐⭐ | Complex questions, best quality |
| gpt-3.5-turbo | ⚡⚡⚡ | 💰     | ⭐⭐       | Budget option                   |

### Google Gemini Models

| Model            | Speed  | Cost | Quality    | Best For                  |
| ---------------- | ------ | ---- | ---------- | ------------------------- |
| gemini-1.5-flash | ⚡⚡⚡ | 💰   | ⭐⭐⭐     | Fast responses, free tier |
| gemini-pro       | ⚡⚡   | 💰💰 | ⭐⭐⭐⭐   | General use               |
| gemini-1.5-pro   | ⚡     | 💰💰 | ⭐⭐⭐⭐⭐ | Complex reasoning         |

### Anthropic Claude Models

| Model           | Speed  | Cost   | Quality    | Best For              |
| --------------- | ------ | ------ | ---------- | --------------------- |
| claude-3-haiku  | ⚡⚡⚡ | 💰     | ⭐⭐⭐     | Fast, budget-friendly |
| claude-3-sonnet | ⚡⚡   | 💰💰   | ⭐⭐⭐⭐   | Balanced performance  |
| claude-3-opus   | ⚡     | 💰💰💰 | ⭐⭐⭐⭐⭐ | Highest quality       |

## Testing

### Test Model Availability

```bash
# Check which models are available
curl http://localhost:8000/models

# Check specific provider
curl http://localhost:8000/models/openai
curl http://localhost:8000/models/google
curl http://localhost:8000/models/anthropic
```

### Test Question Generation

```bash
# Test with OpenAI
curl -X POST http://localhost:8000/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Physics",
    "difficulty": "medium",
    "count": 3,
    "model_provider": "openai",
    "model_name": "gpt-4o-mini"
  }'

# Test with Google Gemini (if API key configured)
curl -X POST http://localhost:8000/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Physics",
    "difficulty": "medium",
    "count": 3,
    "model_provider": "google",
    "model_name": "gemini-1.5-flash"
  }'

# Test with Anthropic Claude (if API key configured)
curl -X POST http://localhost:8000/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Physics",
    "difficulty": "medium",
    "count": 3,
    "model_provider": "anthropic",
    "model_name": "claude-3-haiku-20240307"
  }'
```

## Troubleshooting

### API Key Not Configured

If you see an error about missing API keys:

1. Check that the API key is added to `.env`
2. Restart the backend server: `py main.py`
3. Verify the key is valid by checking the provider's dashboard

### Model Not Available

If a model returns an error:

1. Check the `/models` endpoint to see which models are available
2. Verify your API key has access to that model
3. Some models may require special access or billing setup

### Fallback Behavior

If a model fails, the system automatically falls back to OpenAI GPT-4o-mini (if OpenAI is configured).

## Cost Optimization Tips

1. **Use GPT-4o-mini by default**: Best balance of cost and quality
2. **Try Gemini Flash**: Google offers generous free tier
3. **Reserve GPT-4/Claude Opus**: Use only for complex questions
4. **Adjust temperature**: Lower temperature (0.3-0.5) for factual questions, higher (0.7-0.9) for creative ones

## Frontend Integration (Optional)

To add model selection to your frontend, update the exam configuration form:

```typescript
// Add to your question generation form
const [modelProvider, setModelProvider] = useState("openai");
const [modelName, setModelName] = useState("gpt-4o-mini");

// Fetch available models
useEffect(() => {
  fetch("http://localhost:8000/models")
    .then((res) => res.json())
    .then((data) => {
      // Populate model selection dropdown
    });
}, []);

// Include in API request
const response = await fetch("http://localhost:8000/generate-questions", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    subject,
    difficulty,
    count,
    exam_type,
    model_provider: modelProvider,
    model_name: modelName,
  }),
});
```

## Next Steps

1. **Get API Keys**: Obtain keys for Google Gemini and/or Anthropic Claude
2. **Test Models**: Try different models to compare quality and speed
3. **Monitor Costs**: Track API usage in each provider's dashboard
4. **Optimize**: Choose the best model for your use case and budget
