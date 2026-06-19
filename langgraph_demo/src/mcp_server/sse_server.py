from mcp_server.tools_server import server

if __name__ == "__main__":
    server.run(
        transport="sse",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        path="/sse",
        log_file="server.log",
        log_file_max_size=1024 * 1024 * 1024,
        log_file_max_backups=5,
        log_file_max_age=7,
        log_file_compress=True,
        log_file_rotate_interval=1,
        log_file_rotate_when="H",
        log_file_rotate_mode="m",
    )  # 启动服务
