# African Market Haggling Simulation

A multi-agent negotiation simulation built with Python and Streamlit, developed as an academic assignment on Intelligent Agents. Two BDI (Belief-Desire-Intention) agents — a Seller and a Buyer negotiate the price of everyday goods in a West African market setting. Every decision is deterministic and logic-driven, and you can watch the entire negotiation unfold live, step by step, directly in the browser.

---

## What It Does

The app simulates a price negotiation between two autonomous agents:

- **Amara Diallo (Seller)** — knows his cost price and desired profit margin. He opens with an inflated asking price and lowers it gradually each round, but never below his minimum acceptable price.
- **Fatou Ndiaye (Buyer)** — has a hard budget ceiling and a target price she considers fair. She opens with a low offer and raises it each round, but walks away if the seller stays too high for too long.

The negotiation runs up to 10 rounds. Each round, both agents reason out loud — you see their Beliefs, Desires, and Intentions printed in the interface as each message appears. A live price chart shows the two prices converging (or not) over time. At the end, a banner announces whether a deal was struck or the negotiation broke down.

---

## Agent Architecture

Both agents implement the **BDI (Belief-Desire-Intention)** model of rational agency:

| Component | Description |
|---|---|
| **Belief** | What the agent knows: cost price, current offer, opponent's last move |
| **Desire** | What the agent wants: profit above minimum (seller), fair price under budget (buyer) |
| **Intention** | What the agent commits to doing: concede by a shrinking amount each round |

Concession amounts follow a geometric decay formula:

```
concession = 0.40 × (0.60 ^ round_number) × base_gap
```

This means agents become progressively more stubborn as the negotiation advances — a realistic model of negotiation fatigue. All decisions are fully deterministic; there is no randomness.

These are **goal-based, model-based** agents in the Russell & Norvig taxonomy.

---

## Features

- Live step-by-step rendering — each agent message appears on screen one at a time
- Animated chat bubbles with BDI reasoning tags (Belief / Desire / Intent) visible per message
- Real-time price convergence chart (Plotly) that updates each round
- Configurable speed slider (0.3 s to 2.0 s per step)
- Agent profile cards showing all parameters before the negotiation starts
- Success or failure outcome banner with concession analysis
- Collapsible academic reference section explaining BDI architecture with direct code references
- All prices in FCFA (Central African CFA franc)
- Fully deployable on Hugging Face Spaces (Streamlit SDK)

---

## Project Structure

```
.
├── app.py              # Main application — all agents, simulation logic, and UI
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## How to Use

1. Use the **sidebar** to select the good being sold (Rice, Cooking Oil, or Tomatoes).
2. Set the **Seller parameters**: cost price and desired profit margin.
3. Set the **Buyer parameters**: budget and target price.
4. Adjust the **step speed** slider to control how fast each message appears.
5. Click **Start Negotiation** and watch the agents negotiate in real time.

---

## Deployment on Hugging Face Spaces

This app is ready to deploy on [Hugging Face Spaces](https://huggingface.co/spaces/yopanelly/market-haggling-sim) with the Streamlit SDK.

1. Create a new Space on Hugging Face and select **Streamlit** as the SDK.
2. Upload `app.py` and `requirements.txt` to the Space repository.
3. The Space will build and launch automatically — no modifications needed.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | >= 1.32.0 | Web UI framework and real-time rendering |
| `plotly` | >= 5.20.0 | Interactive price convergence chart |

---

## Academic Context

This project was built as part of a course on **Intelligent Agents**. The simulation demonstrates:

- BDI agent architecture (Bratman, 1987)
- Goal-based and model-based agent design (Russell & Norvig, *Artificial Intelligence: A Modern Approach*)
- Bilateral alternating-offer negotiation protocol
- The Rubinstein bargaining model decreasing patience drives convergence

The collapsible "Agent Architecture Explained" section inside the app maps every BDI concept directly to the variables and methods in the code.

---

## Author

Built by **Yopa Nelly**
Academic assignment Intelligent Agents course
