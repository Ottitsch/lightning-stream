Solution to the coding challenge from Nick Amato (@softwarewithnick)  
https://www.instagram.com/reel/DLVHkauArut/

# Lightning Stream ⚡

A real-time lightning detection client that connects to the Blitzortung.org network and displays live lightning strikes from around the world in your terminal.

## 🌩️ What It Does

This Python script connects to Blitzortung's WebSocket API and streams real-time lightning strike data directly to your console. Watch lightning strikes happen across the globe as they're detected by the community-powered Blitzortung network.


## 📊 Output Format

The script displays each lightning strike on a single line with the following format:

```
Format: [Time] ⚡ Latitude, Longitude | Strike Time | Polarity | Region | Stations | Delay
```

### Example Output

```
[12:46:14] ⚡  29.1579,  -87.5718 | 12:46:10 | - | R0 | 21 stations | 3.8s delay
[12:46:15] ⚡  46.2152,    8.1204 | 12:46:11 | + | R9 | 32 stations | 3.3s delay
[12:46:16] ⚡  35.1796,  -86.0796 | 12:46:12 | - | R3 | 26 stations | 7.2s delay
```

### Field Explanations

- **[Time]** - When the data was received by the script
- **⚡ Latitude, Longitude** - Geographic coordinates where lightning struck
- **Strike Time** - When the lightning actually occurred
- **Polarity** - Electrical charge of the strike (+ positive, - negative)
- **Region** - Geographic region code (0-9)
- **Stations** - Number of detection stations that recorded the strike
- **Delay** - Processing delay from strike detection to the display

## 🌍 About the Data

### Blitzortung Network

[Blitzortung.org](https://www.blitzortung.org) is a worldwide, real-time, community collaborative lightning location network. The network consists of:

- **Volunteer-operated stations** detecting electromagnetic signals from lightning
- **Real-time processing** triangulating strike locations
- **Open data** freely available for research and education


### Data Quality

- **More stations = higher accuracy** - Strikes detected by 20+ stations are very precise
- **Delay varies by location** - Remote areas may have higher processing delays
- **24/7 coverage** - The network operates continuously worldwide

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- `websockets` library

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Ottitsch/lightning-stream.git
cd lightning-stream
```

2. Install dependencies:
```bash
pip install websockets
```

3. Run the script:
```bash
python strike.py
```


## 🛠️ Technical Details

### How It Works

1. **Connects** to `wss://ws1.blitzortung.org/`
2. **Subscribes** by sending `{"a": 111}` message
3. **Receives** obfuscated lightning data
4. **Decodes** the proprietary format to JSON
5. **Displays** formatted strike information


## ⚠️ Disclaimer

This is an educational tool for monitoring lightning activity. Do not use this data for critical weather decisions or safety purposes. Always rely on official weather services for severe weather warnings.

---

**Enjoy watching lightning strikes from around the world! ⚡🌍**
