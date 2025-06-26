#!/usr/bin/env python3
"""
Blitzortung WebSocket Client
Connects to the Blitzortung lightning detection network WebSocket
and prints real-time lightning strike data.
"""

import asyncio
import websockets
import json
from datetime import datetime
import signal
import sys

class BlitzortungClient:
    def __init__(self, uri="wss://ws1.blitzortung.org/"):
        self.uri = uri
        self.websocket = None

    def decode_blitzortung_data(self, data):
        """Decode obfuscated Blitzortung data"""
        try:
            if isinstance(data, str):
                data = data.encode()
            
            e = {}
            d = list(data.decode())
            c = d[0]
            f = c
            g = [c]
            h = 256
            o = h
            
            for i in range(1, len(d)):
                a = ord(d[i])
                a = d[i] if h > a else e.get(a, f + c)
                g.append(a)
                c = a[0] if a else ""
                e[o] = f + c
                o += 1
                f = a
            
            decoded = ''.join(g)
            return json.loads(decoded)
        except Exception as e:
            return None

    async def connect_and_listen(self):
        """Connect to WebSocket and listen for messages"""
        try:
            print(f"Connecting to {self.uri}...")
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                print("Connected! Sending subscription message...")
                
                # Send subscription message to start receiving data
                subscription = json.dumps({"a": 111})
                await websocket.send(subscription)
                print("Subscription sent! Listening for lightning data...")
                print("-" * 60)
                print("Format: [Time] ⚡ Latitude, Longitude | Strike Time | Polarity | Region | Stations | Delay")
                print("-" * 60)
                
                async for message in websocket:
                    await self.handle_message(message)
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by server")
        except Exception as e:
            print(f"Error: {e}")

    async def handle_message(self, message):
        """Process incoming WebSocket messages"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Try to parse as JSON first
            try:
                data = json.loads(message)
                self.print_compact_strike(data, timestamp)
            except json.JSONDecodeError:
                # Try to decode obfuscated Blitzortung data
                decoded_data = self.decode_blitzortung_data(message)
                if decoded_data:
                    self.print_compact_strike(decoded_data, timestamp)
                else:
                    # If not decodable, print as raw text
                    print(f"[{timestamp}] Raw: {message[:100]}{'...' if len(message) > 100 else ''}")
            
        except Exception as e:
            print(f"[{timestamp}] Error: {e}")

    def print_compact_strike(self, data, timestamp):
        """Print lightning strike data in a compact single-line format"""
        if isinstance(data, dict):
            lat = data.get('lat', 0)
            lon = data.get('lon', 0)
            time_us = data.get('time', 0)
            pol = data.get('pol', 0)
            region = data.get('region', 0)
            stations = len(data.get('sig', []))
            delay = data.get('delay', 0)
            
            # Try to convert Blitzortung timestamp to readable time
            strike_time = "??:??:??"
            if time_us:
                try:
                    # Try different timestamp formats
                    # First try as microseconds
                    if time_us > 1e15:  # Very large number, try nanoseconds
                        dt = datetime.fromtimestamp(time_us / 1_000_000_000)
                    elif time_us > 1e12:  # Large number, try microseconds  
                        dt = datetime.fromtimestamp(time_us / 1_000_000)
                    elif time_us > 1e9:   # Normal Unix timestamp
                        dt = datetime.fromtimestamp(time_us)
                    else:
                        dt = None
                    
                    if dt:
                        strike_time = dt.strftime("%H:%M:%S")
                except:
                    # If all else fails, show relative time from now
                    strike_time = f"~{delay:.0f}s ago"
            
            # Format polarity 
            pol_str = "+" if pol == 1 else "-" if pol == 0 else "?"
            
            print(f"[{timestamp}] ⚡ {lat:8.4f}, {lon:9.4f} | {strike_time} | {pol_str} | R{region} | {stations:2d} stations | {delay:.1f}s delay")
        else:
            print(f"[{timestamp}] Non-dict data: {str(data)[:80]}{'...' if len(str(data)) > 80 else ''}")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal. Shutting down...")
    sys.exit(0)

async def main():
    """Main function"""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    client = BlitzortungClient()
    
    try:
        await client.connect_and_listen()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("Blitzortung Lightning Detection WebSocket Client")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    
    # Check if websockets is available
    try:
        import websockets
    except ImportError:
        print("Error: 'websockets' library not found.")
        print("Install it with: pip install websockets")
        sys.exit(1)
    
    # Run the client
    asyncio.run(main())
