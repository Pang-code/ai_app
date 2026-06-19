from mcp_server.tools_server import server

if __name__ == "__main__":
    server.run(
        transport="sse",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        path="/sse",
        log_file="server.log"
    )  # 启动服务
