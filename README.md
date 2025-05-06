
# RazorDB 🔪

**RazorDB** is a lightweight, high-performance key-value store written in Python. It uses raw memory buffers (`mmap`, `memoryview`) for blazing-fast in-memory access and speaks the Redis Serialization Protocol (RESP), making it compatible with clients like `redis-cli`.

---

## ✨ Features

- ⚡️ In-memory, raw binary storage (no Python dicts)
- 🧠 Backed by `mmap` and `memoryview` for zero-copy performance
- 🧵 RESP protocol over TCP — talk to it using `redis-cli`
- 🔌 Commands: `SET`, `GET`, `DEL`
- 🛠 Easy to extend with TTL, persistence, compression

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/razordb.git
cd razordb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # (empty for now)

