from cli import parse_args
from file import read_formation
from handler import create_processes, start_processes


def main():
    """Entry point of the application. This function parses arguments,
    reads the formation file, creates processes and starts those processes"""
    args = parse_args()

    server_ip = args.server_ip
    server_port = args.server_port
    delay = args.player_creation_delay

    players = read_formation(args.formation_file, server_ip, server_port)

    processes = create_processes(players)
    start_processes(processes, delay)


if __name__ == "__main__":
    main()
