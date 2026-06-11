# Perspectum — Regulatory Affairs Dashboard

A read-only dashboard for Perspectum's global medical device clearances and certifications.

## Deploy in 5 minutes (free)

### Option A — Streamlit Community Cloud (recommended)

1. Create a free account at **github.com** and a new public (or private) repository
2. Upload both files: `app.py` and `requirements.txt`
3. Go to **share.streamlit.io** → sign in with GitHub → **Deploy an app**
4. Select your repo, branch `main`, file `app.py` → click **Deploy**
5. You get a permanent URL like `https://yourapp.streamlit.app` — share with clients

Total time: ~5 minutes. No server, no cost.

---

### Option B — Run locally

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

Opens at http://localhost:8501

---

### Option C — Azure Web Apps

1. Create an Azure Web App (Free tier: F1)
2. In **Deployment Center** → connect to GitHub repo
3. Azure auto-deploys on every push
4. Set startup command: `python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## What's included

| Tab | Contents |
|-----|---------|
| 🌍 Overview | Product × jurisdiction matrix + market summary cards |
| 🇺🇸 USA (FDA) | All 10 x 510(k) submissions with timeline chart |
| 🇬🇧 UK (UKCA) | Certificate details + cleared products |
| 🇪🇺 EU (MDR) | EUDAMED device registry |
| 🇸🇬 Singapore | HSA — all 5 products exempt |
| 🇲🇾 Malaysia | MDA registration numbers |
| 🇦🇪 UAE | MOHAP clearances (March 2026) |
| 🇨🇭 Switzerland | Swissmedic via EU MDR MRA |
| 📋 All Clearances | Searchable, filterable master table + CSV download |
| 📊 Analytics | Charts: by market, product, authority, FDA timeline |

## Files

| File | Purpose |
|------|---------|
| `app.py` | The full Streamlit dashboard |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |
