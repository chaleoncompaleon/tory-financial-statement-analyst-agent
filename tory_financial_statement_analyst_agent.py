from uagents import Agent, Context, Protocol, Model
import requests

# Define request and response models
class FinancialsRequest(Model):
    uuid: str
    timestamp: int
    token: str

class FinancialsResponse(Model):
    uuid: str
    timestamp: int
    summary: str

# Instantiate the agent
financials_agent = Agent(
  name="financials_agent",
  seed="SECRET_SEED"
)

# Create a protocol instance
financials_protocol = Protocol("FinancialsProtocol")

# Message handler
@financials_protocol.on_message(model=FinancialsRequest)
async def handle_financials_request(ctx: Context, sender: str, msg: FinancialsRequest):
    ctx.logger.info(f"[FinancialsAgent] ✅ Received Financials Request: {msg.uuid} at {msg.timestamp}")

    # Prepare ASI Completion API payload
    request_data = {
        "model": "asi1-mini",
        "temperature": 0,
        "stream": False,
        "max_tokens": 100000,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional hedge fund manager analyzing crypto economic metrics. Your job is to synthesize market signals and extract **insightful**, **quantitative** outlooks.\n\nBefore responding, follow this logic:\n\n1. Group metrics by theme: usage (users, txs), developer activity, token economy (fees, incentives), valuation (market cap, price, P/F, P/S).\n2. Identify changes >10% and correlate them (e.g., falling DAU + falling price = bearish demand).\n3. Add brief insight into **why** a change matters — how it may signal strength, weakness, or divergence.\n4. Use prior data to suggest **future market direction** (e.g., revenue down 70% 3 months in a row = negative trend).\n5. Return only a raw JSON object in this format:\n\n{\"bullishThoughts\":[\"...\"],\"bearishThoughts\":[\"...\"]}\n\nRules:\n- Use at least **3 bullet points per section**.\n- Each point must include metric name, change (% or value), and why it matters.\n- Avoid vague language — use data-backed, strategic thinking only.\n- Do NOT return anything except the single-line JSON response.\n- Do NOT wrap your response in code blocks like ```json. Only return raw valid JSON without any prefix or suffix."
            },
            {"role": "user", "content": "Please analyze the following dataset:"},
            {"role": "user", "content": msg.token}
        ]
    }

    try:
        ctx.logger.info("🌐 Calling ASI financial analysis API...")
        response = requests.post(
            url='https://api.asi1.ai/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY'
            },
            json=request_data
        )
        response.raise_for_status()
        result = response.json()
        summary = result['choices'][0]['message']['content']
        ctx.logger.info("✅ ASI response received successfully.")
    except Exception as e:
        ctx.logger.error(f"❌ Financials analysis failed: {e}")
        summary = "Financial statement analysis unavailable."

    # Send response back
    ctx.logger.info("📤 Sending FinancialsResponse back to coordinator...")
    await ctx.send(sender, FinancialsResponse(
        uuid=msg.uuid,
        timestamp=msg.timestamp,
        summary=summary
    ))

# Register protocol
financials_agent.include(financials_protocol)

# Run agent
if __name__ == "__main__":
    financials_agent.run()
