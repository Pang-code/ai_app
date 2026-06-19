from mcp_server.tools_server import server

if __name__ == "__main__":
    server.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        path="/streamable"
    )  # 启动服务
