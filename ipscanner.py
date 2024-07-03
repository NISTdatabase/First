import asyncio
import socket
import aioping

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Unable to get local IP: {e}")
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

# Function to generate IP range
def generate_ip_range(local_ip):
    ip_parts = local_ip.split('.')
    base_ip = '.'.join(ip_parts[:3]) + '.'
    return [base_ip + str(i) for i in range(1, 255)]

# Asynchronous function to ping an IP address
async def ping_ip(ip, semaphore):
    async with semaphore:
        try:
            delay = await aioping.ping(ip, timeout=1)
            print(f'{ip} is active')
        except TimeoutError:
            pass
        except OSError as e:
            if e.errno == 65:  # No route to host
                pass
            else:
                print(f'Error pinging {ip}: {e}')

# Asynchronous function to scan the IP range
async def scan_ip_range(ip_range, max_concurrent_tasks=100):
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    tasks = [ping_ip(ip, semaphore) for ip in ip_range]
    await asyncio.gather(*tasks)

# Main function to initiate scanning
if __name__ == '__main__':
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        print("Failed to obtain local IP address. Exiting.")
    else:
        print(f'Local IP: {local_ip}')
        ip_range = generate_ip_range(local_ip)
        print('Scanning IP range...')
        asyncio.run(scan_ip_range(ip_range))
        print('Scan complete.')

