import asyncio
from memstore import MemoryKVStore

store = MemoryKVStore()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")

    while not reader.at_eof():
        try:
            cmd = await parse_resp_command(reader)
            if not cmd:
                continue
            response = handle_command(cmd)
            writer.write(response)
            await writer.drain()
        except Exception as e:
            print(f"Error: {e}")
            break

    writer.close()
    await writer.wait_closed()

async def parse_resp_command(reader):
    line = await reader.readline()
    if not line or not line.startswith(b'*'):
        return None
    num_args = int(line[1:].strip())
    args = []
    for _ in range(num_args):
        await reader.readline()  # Skip length line
        arg = await reader.readline()
        args.append(arg.strip())
    return args

def handle_command(cmd):
    if not cmd:
        return b"-ERR empty command\r\n"

    op = cmd[0].upper()
    if op == b'SET' and len(cmd) == 3:
        store.set(cmd[1].decode(), cmd[2])
        return b"+OK\r\n"
    elif op == b'GET' and len(cmd) == 2:
        val = store.get(cmd[1].decode())
        if val is None:
            return b"$-1\r\n"
        return f"${len(val)}\r\n".encode() + val + b"\r\n"
    elif op == b'DEL' and len(cmd) == 2:
        store.delete(cmd[1].decode())
        return b":1\r\n"
    else:
        return b"-ERR unknown command or wrong args\r\n"

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 6380)
    print("Server running on port 6380...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
