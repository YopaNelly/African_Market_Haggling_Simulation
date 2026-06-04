import streamlit as st
import plotly.graph_objects as go
import time
import re

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="African Market Haggling Simulation",
    page_icon=None,
    layout="wide",
)

# ─────────────────────────────────────────────
#  STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem; color: #1a1a2e; margin-bottom: 0.1rem;
}
.sub-title { font-size: 0.95rem; color: #777; margin-bottom: 1.5rem; }

.card-seller {
    background: linear-gradient(135deg, #7c3900, #b85c00);
    color: #fff8f0; border-radius: 14px; padding: 1.4rem 1.6rem;
    box-shadow: 0 6px 24px rgba(120,57,0,0.25);
}
.card-buyer {
    background: linear-gradient(135deg, #003f5c, #0077b6);
    color: #f0f8ff; border-radius: 14px; padding: 1.4rem 1.6rem;
    box-shadow: 0 6px 24px rgba(0,63,92,0.25);
}
.card-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.7; margin-bottom: 0.2rem; }
.card-name  { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700;
              border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 0.4rem; margin-bottom: 0.7rem; }
.card-row   { display: flex; justify-content: space-between; margin: 0.3rem 0; font-size: 0.9rem; }
.card-key   { opacity: 0.8; }
.card-val   { font-weight: 600; }

.round-header {
    text-align: center; font-family: 'Playfair Display', serif;
    font-size: 0.8rem; color: #999; letter-spacing: 0.12em;
    text-transform: uppercase; margin: 1.2rem 0 0.5rem 0;
    border-bottom: 1px solid #e8e8e8; padding-bottom: 0.35rem;
}

.bubble-seller {
    background: #fff5e8; border: 1.5px solid #d4904a;
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.1rem; margin: 0.35rem 0 0.35rem 18%;
    box-shadow: 0 2px 10px rgba(180,100,0,0.09);
    animation: fadeSlideLeft 0.4s ease;
}
.bubble-buyer {
    background: #e8f4ff; border: 1.5px solid #4a90c4;
    border-radius: 16px 16px 16px 4px;
    padding: 0.85rem 1.1rem; margin: 0.35rem 18% 0.35rem 0;
    box-shadow: 0 2px 10px rgba(0,80,160,0.09);
    animation: fadeSlideRight 0.4s ease;
}
.bubble-eval {
    background: #f8f0e8; border: 1px dashed #c4804a;
    border-radius: 8px; font-size: 0.82rem; color: #6a3a0a;
    padding: 0.45rem 1rem; margin: 0.15rem 0 0.15rem 18%;
    font-style: italic;
}
.bubble-walkaway {
    background: #fff0f0; border: 1.5px solid #c0392b;
    border-radius: 12px; padding: 0.85rem 1.1rem;
    margin: 0.35rem 18% 0.35rem 0;
    animation: fadeSlideRight 0.4s ease;
}
.bubble-deal {
    text-align: center; padding: 1rem 1.5rem;
    background: linear-gradient(90deg, #e8f8ef, #d0f0df);
    border: 2px solid #28a745; border-radius: 12px; margin-top: 0.8rem;
    animation: fadeSlideLeft 0.5s ease;
}

@keyframes fadeSlideLeft {
    from { opacity: 0; transform: translateX(18px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeSlideRight {
    from { opacity: 0; transform: translateX(-18px); }
    to   { opacity: 1; transform: translateX(0); }
}

.bubble-agent { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 0.2rem; }
.seller-name  { color: #7c3900; }
.buyer-name   { color: #003f5c; }
.walkaway-name{ color: #7c0a0a; }
.bubble-price { font-family: 'Playfair Display', serif; font-size: 1.3rem; margin-bottom: 0.25rem; }
.bubble-reason {
    font-size: 0.84rem; color: #444;
    border-top: 1px solid rgba(0,0,0,0.08);
    padding-top: 0.35rem; margin-top: 0.25rem; line-height: 1.55;
}
.bdi-tag { display: inline-block; font-size: 0.65rem; font-weight: 700;
           letter-spacing: 0.07em; border-radius: 4px; padding: 1px 5px; margin-right: 3px; }
.tag-b { background: #d4e8ff; color: #003f8c; }
.tag-d { background: #ffe8d4; color: #8c3f00; }
.tag-i { background: #d4ffd4; color: #006600; }

.banner-success {
    background: linear-gradient(90deg, #1a6b3c, #28a745);
    color: white; border-radius: 12px; padding: 1.5rem 2rem;
    text-align: center; box-shadow: 0 4px 20px rgba(40,167,69,0.3); margin-top: 1.2rem;
}
.banner-fail {
    background: linear-gradient(90deg, #7c0a0a, #c0392b);
    color: white; border-radius: 12px; padding: 1.5rem 2rem;
    text-align: center; box-shadow: 0 4px 20px rgba(192,57,43,0.3); margin-top: 1.2rem;
}
.banner-title { font-family: 'Playfair Display', serif; font-size: 1.5rem; margin-bottom: 0.4rem; }
.banner-body  { font-size: 0.95rem; opacity: 0.92; }

.status-bar {
    background: #1a1a2e; color: #f0c060;
    border-radius: 8px; padding: 0.5rem 1rem;
    font-size: 0.85rem; text-align: center; margin-bottom: 0.8rem;
    font-family: 'Playfair Display', serif; letter-spacing: 0.05em;
}

section[data-testid="stSidebar"] { background: #1a1a2e; }
section[data-testid="stSidebar"] label { color: #d0d0e0 !important; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BDI AGENT CLASSES
# ─────────────────────────────────────────────

class SellerAgent:
    def __init__(self, good, cost_price, margin_pct):
        self.good          = good
        self.cost_price    = cost_price
        self.margin_pct    = margin_pct
        self.opening_price = round(cost_price * (1 + margin_pct / 100 + 0.25))
        self.minimum_price = round(cost_price * (1 + margin_pct / 100))
        self.current_ask   = self.opening_price
        self.buyer_last_offer = None
        self.round_number  = 0
        self.target_price  = self.minimum_price + round((self.opening_price - self.minimum_price) * 0.3)

    def bdi_reason(self):
        belief = (f"Cost is {self.cost_price:,.0f} FCFA. "
                  f"Minimum acceptable: {self.minimum_price:,.0f} FCFA. "
                  f"Current ask: {self.current_ask:,.0f} FCFA.")
        if self.buyer_last_offer:
            belief += f" Buyer last offered {self.buyer_last_offer:,.0f} FCFA."
        desire = (f"I must clear at least {self.minimum_price:,.0f} FCFA. "
                  f"I ideally want above {self.target_price:,.0f} FCFA.")
        concession = self._concession_amount()
        intention = (f"I will concede {concession:,.0f} FCFA this round. "
                     f"My stubbornness increases each round.")
        return belief, desire, intention

    def _concession_amount(self):
        base_gap = self.opening_price - self.minimum_price
        factor   = 0.40 * (0.60 ** self.round_number)
        return max(round(base_gap * factor), 1)

    def make_offer(self):
        self.round_number += 1
        if self.round_number == 1:
            return self.opening_price, *self.bdi_reason()
        new_ask = max(self.current_ask - self._concession_amount(), self.minimum_price)
        self.current_ask = new_ask
        return new_ask, *self.bdi_reason()

    def evaluate_buyer_offer(self, buyer_offer):
        self.buyer_last_offer = buyer_offer
        if buyer_offer >= self.minimum_price:
            return True, f"Offer of {buyer_offer:,.0f} FCFA meets my minimum. I accept."
        return False, f"Offer of {buyer_offer:,.0f} FCFA is below my minimum of {self.minimum_price:,.0f} FCFA. Not acceptable."


class BuyerAgent:
    def __init__(self, good, budget, target_price, walk_away_rounds=5):
        self.good                = good
        self.budget              = budget
        self.target_price        = target_price
        self.opening_offer       = round(target_price * 0.70)
        self.current_offer       = self.opening_offer
        self.seller_last_ask     = None
        self.round_number        = 0
        self.walk_away_rounds    = walk_away_rounds
        self.rounds_above_budget = 0

    def bdi_reason(self):
        belief = (f"Budget ceiling: {self.budget:,.0f} FCFA. "
                  f"Fair value: {self.target_price:,.0f} FCFA. "
                  f"My current offer: {self.current_offer:,.0f} FCFA.")
        if self.seller_last_ask:
            belief += f" Seller is asking {self.seller_last_ask:,.0f} FCFA."
        desire = (f"I want to pay no more than {self.target_price:,.0f} FCFA, "
                  f"hard ceiling at {self.budget:,.0f} FCFA.")
        concession = self._concession_amount()
        intention = (f"I will raise my offer by {concession:,.0f} FCFA. "
                     f"My patience is decreasing each round.")
        return belief, desire, intention

    def _concession_amount(self):
        base_gap = self.target_price - self.opening_offer
        factor   = 0.40 * (0.60 ** self.round_number)
        return max(round(base_gap * factor), 1)

    def make_offer(self, seller_ask):
        self.seller_last_ask = seller_ask
        self.round_number   += 1
        if seller_ask > self.budget:
            self.rounds_above_budget += 1
        else:
            self.rounds_above_budget = 0
        if self.round_number == 1:
            return self.opening_offer, *self.bdi_reason()
        new_offer = min(self.current_offer + self._concession_amount(), self.budget)
        self.current_offer = new_offer
        return new_offer, *self.bdi_reason()

    def should_walk_away(self):
        if self.rounds_above_budget >= self.walk_away_rounds:
            return True, (f"Seller has stayed above my budget of {self.budget:,.0f} FCFA "
                          f"for {self.rounds_above_budget} consecutive rounds. I am leaving.")
        if self.round_number >= 10:
            return True, "Ten rounds completed with no agreement. I am walking away."
        return False, ""


# ─────────────────────────────────────────────
#  SIMULATE ALL EVENTS AT ONCE
# ─────────────────────────────────────────────

def compute_all_events(good, cost_price, margin_pct, budget, target_price):
    seller = SellerAgent(good, cost_price, margin_pct)
    buyer  = BuyerAgent(good, budget, target_price, walk_away_rounds=5)

    events        = []
    seller_prices = []
    buyer_prices  = []
    outcome = "no_deal"
    deal_price = deal_round = None
    walk_reason = who = ""

    for round_num in range(1, 11):
        # --- Seller speaks ---
        s_price, s_bel, s_des, s_int = seller.make_offer()
        seller_prices.append(s_price)
        events.append({"type": "seller_offer", "round": round_num,
                        "price": s_price, "belief": s_bel, "desire": s_des, "intention": s_int})

        # --- Buyer decides whether to walk before responding ---
        walk, walk_reason = buyer.should_walk_away()
        if walk:
            events.append({"type": "walk_away", "round": round_num, "reason": walk_reason})
            break

        # --- Buyer responds ---
        b_price, b_bel, b_des, b_int = buyer.make_offer(s_price)
        buyer_prices.append(b_price)
        events.append({"type": "buyer_offer", "round": round_num,
                        "price": b_price, "belief": b_bel, "desire": b_des, "intention": b_int})

        # --- Check if prices met ---
        if b_price >= s_price:
            deal_price = round((b_price + s_price) / 2)
            deal_round = round_num
            outcome    = "deal"
            sc = seller.opening_price - s_price
            bc = b_price - buyer.opening_offer
            who = ("The Seller made larger concessions." if sc > bc
                   else "The Buyer made larger concessions." if bc > sc
                   else "Both agents conceded equally.")
            events.append({"type": "deal", "price": deal_price, "round": deal_round, "who": who})
            break

        # --- Seller evaluates buyer offer ---
        accepted, eval_msg = seller.evaluate_buyer_offer(b_price)
        events.append({"type": "seller_eval", "round": round_num, "msg": eval_msg})
        if accepted:
            deal_price = b_price
            deal_round = round_num
            outcome    = "deal"
            sc = seller.opening_price - s_price
            bc = b_price - buyer.opening_offer
            who = ("The Seller made larger concessions." if sc > bc
                   else "The Buyer made larger concessions." if bc > sc
                   else "Both agents conceded equally.")
            events.append({"type": "deal", "price": deal_price, "round": deal_round, "who": who})
            break
    else:
        walk_reason = "Ten rounds elapsed without agreement."
        events.append({"type": "walk_away", "round": 10, "reason": walk_reason})

    return dict(events=events, seller_prices=seller_prices, buyer_prices=buyer_prices,
                outcome=outcome, deal_price=deal_price, deal_round=deal_round,
                walk_reason=walk_reason, who_conceded_more=who)


# ─────────────────────────────────────────────
#  HTML RENDERERS
# ─────────────────────────────────────────────

def html_bubble(agent, price, belief, desire, intention):
    cls      = "bubble-seller" if agent == "seller" else "bubble-buyer"
    name_cls = "seller-name"   if agent == "seller" else "buyer-name"
    label    = "Amara Diallo — Seller" if agent == "seller" else "Fatou Ndiaye — Buyer"
    return f"""<div class="{cls}">
  <div class="bubble-agent {name_cls}">{label}</div>
  <div class="bubble-price">{price:,.0f} FCFA</div>
  <div class="bubble-reason">
    <span class="bdi-tag tag-b">BELIEF</span> {belief}<br>
    <span class="bdi-tag tag-d">DESIRE</span> {desire}<br>
    <span class="bdi-tag tag-i">INTENT</span> {intention}
  </div>
</div>"""


def html_eval(msg):
    return f'<div class="bubble-eval">{msg}</div>'


def html_walk(reason):
    return f"""<div class="bubble-walkaway">
  <div class="bubble-agent walkaway-name">Fatou Ndiaye — Walking Away</div>
  <div class="bubble-reason">{reason}</div>
</div>"""


def html_deal(price, rnd):
    return f"""<div class="bubble-deal">
  <strong style="color:#1a6b3c; font-family:'Playfair Display',serif; font-size:1.25rem;">
    Deal Struck at {price:,} FCFA — Round {rnd}
  </strong>
</div>"""


def html_round_header(rnd):
    return f'<div class="round-header">Round {rnd}</div>'


def build_chart(seller_prices, buyer_prices, deal_round=None, deal_price=None):
    fig = go.Figure()
    if seller_prices:
        fig.add_trace(go.Scatter(
            x=list(range(1, len(seller_prices)+1)), y=seller_prices,
            mode="lines+markers", name="Seller Ask",
            line=dict(color="#b85c00", width=2.5), marker=dict(size=8)))
    if buyer_prices:
        fig.add_trace(go.Scatter(
            x=list(range(1, len(buyer_prices)+1)), y=buyer_prices,
            mode="lines+markers", name="Buyer Offer",
            line=dict(color="#0077b6", width=2.5), marker=dict(size=8)))
    if deal_round and deal_price:
        fig.add_trace(go.Scatter(
            x=[deal_round], y=[deal_price], mode="markers+text",
            name="Deal", marker=dict(size=20, color="#28a745", symbol="star"),
            text=[f"DEAL {deal_price:,}"], textposition="top center",
            textfont=dict(size=11, color="#28a745")))
    fig.update_layout(
        title=dict(text="Price Convergence", font=dict(family="Playfair Display", size=17), x=0.02),
        xaxis=dict(title="Round", tickmode="linear", dtick=1, gridcolor="#eee"),
        yaxis=dict(title="Price (FCFA)", gridcolor="#eee", tickformat=",.0f"),
        plot_bgcolor="#fafafa", paper_bgcolor="#fff",
        legend=dict(orientation="h", y=-0.22),
        margin=dict(t=50, b=50, l=55, r=20), height=340,
    )
    return fig


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────

def reset_state():
    st.session_state.update(
        running=False, step=0, sim_data=None,
        bubbles=[], seller_prices=[], buyer_prices=[],
        deal_round=None, deal_price=None, done=False,
        last_round_shown=0,
    )

for key, val in dict(running=False, step=0, sim_data=None,
                      bubbles=[], seller_prices=[], buyer_prices=[],
                      deal_round=None, deal_price=None, done=False,
                      last_round_shown=0).items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("<h2 style='color:#f0c060;font-family:Playfair Display,serif;'>Controls</h2>",
                unsafe_allow_html=True)
    good         = st.selectbox("Good being sold",
                                ["Rice (50 kg bag)", "Cooking Oil (20 L)", "Tomatoes (1 basket)"])
    st.markdown("---")
    st.markdown("<p style='color:#aaa;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.1em;'>Seller</p>",
                unsafe_allow_html=True)
    cost_price   = st.slider("Cost Price (FCFA)",        1000, 30000,  8000, 500)
    margin_pct   = st.slider("Desired Margin (%)",         10,    80,    40,   5)
    st.markdown("---")
    st.markdown("<p style='color:#aaa;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.1em;'>Buyer</p>",
                unsafe_allow_html=True)
    budget       = st.slider("Buyer Budget (FCFA)",       2000, 40000, 12000, 500)
    target_price = st.slider("Buyer Target Price (FCFA)", 1000, 30000, 10000, 500)
    st.markdown("---")
    start_btn    = st.button("Start Negotiation", use_container_width=True, type="primary")
    speed        = st.select_slider("Step speed (seconds)", options=[0.3, 0.5, 0.8, 1.2, 2.0], value=0.8)


# ─────────────────────────────────────────────
#  HEADER + PROFILE CARDS
# ─────────────────────────────────────────────

st.markdown("<div class='main-title'>African Market Haggling Simulation</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>BDI Multi-Agent Negotiation — Academic Demonstration</div>", unsafe_allow_html=True)

opening_ask = round(cost_price * (1 + margin_pct / 100 + 0.25))
minimum_ask = round(cost_price * (1 + margin_pct / 100))
opening_bid = round(target_price * 0.70)

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""<div class="card-seller">
  <div class="card-label">Agent Profile</div>
  <div class="card-name">Amara Diallo</div>
  <div class="card-row"><span class="card-key">Good</span><span class="card-val">{good}</span></div>
  <div class="card-row"><span class="card-key">Cost Price</span><span class="card-val">{cost_price:,} FCFA</span></div>
  <div class="card-row"><span class="card-key">Opening Ask</span><span class="card-val">{opening_ask:,} FCFA</span></div>
  <div class="card-row"><span class="card-key">Minimum Price</span><span class="card-val">{minimum_ask:,} FCFA</span></div>
  <div class="card-row"><span class="card-key">Desired Margin</span><span class="card-val">{margin_pct}%</span></div>
</div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="card-buyer">
  <div class="card-label">Agent Profile</div>
  <div class="card-name">Fatou Ndiaye</div>
  <div class="card-row"><span class="card-key">Good</span><span class="card-val">{good}</span></div>
  <div class="card-row"><span class="card-key">Budget</span><span class="card-val">{budget:,} FCFA</span></div>
  <div class="card-row"><span class="card-key">Target Price</span><span class="card-val">{target_price:,} FCFA</span></div>
  <div class="card-row"><span class="card-key">Opening Offer</span><span class="card-val">{opening_bid:,} FCFA</span></div>
  <div class="card-row"><span class="card-key">Walk-Away</span><span class="card-val">After 5 rounds above budget</span></div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  START BUTTON — load sim, begin replay
# ─────────────────────────────────────────────

if start_btn:
    reset_state()
    st.session_state.sim_data = compute_all_events(good, cost_price, margin_pct, budget, target_price)
    st.session_state.running  = True
    st.rerun()


# ─────────────────────────────────────────────
#  STEP PROCESSOR
#  Each rerun processes exactly ONE event,
#  renders it, sleeps, then reruns again.
# ─────────────────────────────────────────────

if st.session_state.running and not st.session_state.done:
    sim    = st.session_state.sim_data
    events = sim["events"]
    step   = st.session_state.step

    if step < len(events):
        event = events[step]

        # Build the HTML piece for this single event
        if event["type"] == "seller_offer":
            rnd = event["round"]
            if rnd != st.session_state.last_round_shown:
                st.session_state.bubbles.append(html_round_header(rnd))
                st.session_state.last_round_shown = rnd
            st.session_state.bubbles.append(
                html_bubble("seller", event["price"], event["belief"], event["desire"], event["intention"]))
            st.session_state.seller_prices.append(event["price"])

        elif event["type"] == "buyer_offer":
            st.session_state.bubbles.append(
                html_bubble("buyer", event["price"], event["belief"], event["desire"], event["intention"]))
            st.session_state.buyer_prices.append(event["price"])

        elif event["type"] == "seller_eval":
            st.session_state.bubbles.append(html_eval(event["msg"]))

        elif event["type"] == "walk_away":
            st.session_state.bubbles.append(html_walk(event["reason"]))
            st.session_state.done = True

        elif event["type"] == "deal":
            st.session_state.deal_price = event["price"]
            st.session_state.deal_round = event["round"]
            st.session_state.bubbles.append(html_deal(event["price"], event["round"]))
            st.session_state.done = True

        st.session_state.step += 1


# ─────────────────────────────────────────────
#  RENDER — status bar, chat, chart
# ─────────────────────────────────────────────

if st.session_state.running or st.session_state.done:
    sim = st.session_state.sim_data

    # Status bar
    total_events = len(sim["events"]) if sim else 0
    step         = st.session_state.step
    if not st.session_state.done:
        st.markdown(f"<div class='status-bar'>Negotiating... event {step} of {total_events}</div>",
                    unsafe_allow_html=True)
    else:
        result_word = "Deal reached" if sim["outcome"] == "deal" else "No deal"
        st.markdown(f"<div class='status-bar'>Simulation complete — {result_word}</div>",
                    unsafe_allow_html=True)

    # Chat transcript
    if st.session_state.bubbles:
        st.markdown("".join(st.session_state.bubbles), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Price chart
    if st.session_state.seller_prices:
        fig = build_chart(
            st.session_state.seller_prices,
            st.session_state.buyer_prices,
            st.session_state.deal_round,
            st.session_state.deal_price,
        )
        st.plotly_chart(fig, use_container_width=True, key="price_chart")

    # Outcome banner (only when done)
    if st.session_state.done:
        if sim["outcome"] == "deal":
            st.markdown(f"""<div class="banner-success">
  <div class="banner-title">Deal Successfully Reached</div>
  <div class="banner-body">
    Final price: <strong>{sim['deal_price']:,} FCFA</strong>
    &nbsp;|&nbsp; Rounds: <strong>{sim['deal_round']}</strong>
    &nbsp;|&nbsp; {sim['who_conceded_more']}
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="banner-fail">
  <div class="banner-title">Negotiation Broke Down</div>
  <div class="banner-body">{sim['walk_reason']}</div>
</div>""", unsafe_allow_html=True)

    # Trigger next step if not done
    if not st.session_state.done:
        time.sleep(speed)
        st.rerun()

else:
    st.info("Set your parameters in the sidebar and click Start Negotiation.")


# ─────────────────────────────────────────────
#  ACADEMIC SECTION
# ─────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)

with st.expander("Agent Architecture Explained (Academic Reference)"):
    st.markdown("""
## BDI Architecture in This Simulation

### What is BDI?
**BDI** stands for **Belief-Desire-Intention**, a model of rational agency from Michael Bratman's theory of practical reasoning:
- **Beliefs** — the agent's information about the world.
- **Desires** — the agent's goals and motivations.
- **Intentions** — the committed plan of action to achieve those goals.

---

### SellerAgent

| State | Code | Meaning |
|---|---|---|
| Belief | `self.cost_price`, `self.current_ask`, `self.buyer_last_offer` | What the seller knows about the situation |
| Desire | `self.minimum_price`, `self.target_price` | Sell above minimum; ideally above target |
| Intention | `make_offer()`, `_concession_amount()` | Lower ask each round by a shrinking amount |

### BuyerAgent

| State | Code | Meaning |
|---|---|---|
| Belief | `self.budget`, `self.seller_last_ask`, `self.target_price` | What the buyer perceives |
| Desire | `self.budget` (hard ceiling), `self.target_price` | Pay fair price, never exceed budget |
| Intention | `make_offer()`, `should_walk_away()` | Raise offer each round; leave if seller stays too high |

---

### Agent Type
These are **goal-based, model-based** agents (Russell & Norvig):
- **Model-based**: internal state tracks history across rounds.
- **Goal-based**: decisions are driven by declared objectives, not reflexes.
- **Rational**: concession formula `0.40 * (0.60 ** round) * base_gap` ensures deterministic, diminishing flexibility — agents get more stubborn as rounds progress, mimicking real human negotiation fatigue.

### Protocol
Bilateral alternating-offer protocol, max 10 rounds. Deal when `buyer_offer >= seller_ask`. No deal if buyer walks after 5 rounds above budget or rounds run out.
    """)
