from enhancements.modules import ModuleParser
from enhancements.plugins import LogModule

from udp_proxy_server.udpconverter import UDPConverter


def udp2tcp():

    moduleloader = ModuleParser(description='UDP 2 TCP Converter')
    moduleloader.add_plugin(LogModule)

    moduleloader.add_argument(
        '-li', '--listenip',
        dest='listen_ip',
        default='0.0.0.0',  # nosec
        help='IP address to listen for incoming data'
    )
    moduleloader.add_argument(
        '-lp',
        '--listenport',
        dest='listen_port',
        type=int,
        required=True,
        help='port to listen on'
    )
    moduleloader.add_argument(
        '-ti',
        '--targetip',
        dest='target_ip',
        required=True,
        help='remote target IP'
    )
    moduleloader.add_argument(
        '-tp',
        '--targetport',
        dest='target_port',
        type=int,
        required=True,
        help='remote target port'
    )
    moduleloader.add_argument(
        '--multicast-group',
        dest='multicast_group',
        help='multicast group address'
    )
    moduleloader.add_argument(
        '--single-connection',
        dest='single_connection',
        action='store_true',
        default=False,
        help='use a single connection for tcp, no response possible'
    )
    args = moduleloader.parse_args()

    converter = UDPConverter(
        (args.listen_ip, args.listen_port),
        (args.target_ip, args.target_port),
        multicast_group=args.multicast_group,
        single_connection=args.single_connection
    )
    converter.run()
