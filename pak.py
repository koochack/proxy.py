import ctypes
from ctypes import wintypes, byref
from ctypes.wintypes import DWORD, HANDLE, BOOL, ULONG, ULARGE_INTEGER, LPCWSTR, BOOLEAN, BYTE

# Load the Wintun library
wintun = ctypes.WinDLL('./wintun/bin/amd64/wintun.dll')
iphlpapi = ctypes.WinDLL('Iphlpapi.dll')


# Define the return type and argument types of the methods

class MIB_IPINTERFACE_ROW(ctypes.Structure):
    _fields_ = [
        ("Family", ULONG),
        ("InterfaceLuid", ULARGE_INTEGER),
        ("InterfaceIndex", ULONG),
        ("MaxReassemblySize", ULONG),
        ("InterfaceIdentifier", ctypes.c_ulonglong),
        ("MinRouterAdvertisementInterval", ULONG),
        ("MaxRouterAdvertisementInterval", ULONG),
        ("AdvertisingEnabled", BOOLEAN),
        ("ForwardingEnabled", BOOLEAN),
        ("WeakHostSend", BOOLEAN),
        ("WeakHostReceive", BOOLEAN),
        ("UseAutomaticMetric", BOOLEAN),
        ("UseNeighborUnreachabilityDetection", BOOLEAN),
        ("ManagedAddressConfigurationSupported", BOOLEAN),
        ("OtherStatefulConfigurationSupported", BOOLEAN),
        ("AdvertiseDefaultRoute", BOOLEAN),
        ("RouterDiscoveryBehavior", ULONG),
        ("DadTransmits", ULONG),
        ("BaseReachableTime", ULONG),
        ("RetransmitTime", ULONG),
        ("PathMtuDiscoveryTimeout", ULONG),
        ("LinkLocalAddressBehavior", ULONG),
        ("LinkLocalAddressTimeout", ULONG),
        ("ZoneIndices", ULONG * 16),
        ("SitePrefixLength", ULONG),
        ("Metric", ULONG),
        ("NlMtu", ULONG),
        ("Connected", BOOLEAN),
        ("SupportsWakeUpPatterns", BOOLEAN),
        ("SupportsNeighborDiscovery", BOOLEAN),
        ("SupportsRouterDiscovery", BOOLEAN),
        ("ReachableTime", ULONG),
        ("TransmitOffload", ULONG),
        ("ReceiveOffload", ULONG),
        ("DisableDefaultRoutes", BOOLEAN),
    ]



# WintunCreateAdapter(const WCHAR *AdapterName, const GUID *TunnelType, const GUID *RequestedGUID, GUID *AllocatedGUID,
# DWORD *LastError)
wintun.WintunCreateAdapter.restype = HANDLE
wintun.WintunCreateAdapter.argtypes = [LPCWSTR, ctypes.POINTER(ctypes.c_ubyte * 16),
                                       ctypes.POINTER(ctypes.c_ubyte * 16), ctypes.POINTER(ctypes.c_ubyte * 16),
                                       ctypes.POINTER(DWORD)]

# WintunDeleteAdapter(HANDLE Adapter)
wintun.WintunCloseAdapter.restype = BOOL
wintun.WintunCloseAdapter.argtypes = [HANDLE]

wintun.WintunGetAdapterLUID.restype = BOOL
wintun.WintunGetAdapterLUID.argtypes = [HANDLE, ctypes.POINTER(DWORD)]

wintun.WintunStartSession.restype = BOOL
wintun.WintunStartSession.argtypes = [HANDLE, ctypes.POINTER(DWORD)]

wintun.WintunAllocateSendPacket.restype = BOOL
wintun.WintunAllocateSendPacket.argtypes = [HANDLE, ctypes.POINTER(DWORD)]

wintun.WintunSendPacket.restype = BOOL
wintun.WintunSendPacket.argtypes = [HANDLE, ctypes.POINTER(BYTE)]

wintun.WintunReleaseReceivePacket.restype = BOOL
wintun.WintunReleaseReceivePacket.argtypes = [HANDLE, ctypes.POINTER(BYTE)]

wintun.WintunReceivePacket.restype = BOOL
wintun.WintunReceivePacket.argtypes = [HANDLE, ctypes.POINTER(DWORD)]

iphlpapi.InitializeIpInterfaceEntry.restype = None
iphlpapi.InitializeIpInterfaceEntry.argtypes = [ctypes.c_void_p]

iphlpapi.SetIpInterfaceEntry.restype = DWORD
iphlpapi.SetIpInterfaceEntry.argtypes = [ctypes.c_void_p]

iphlpapi.GetIpInterfaceEntry.restype = DWORD
iphlpapi.GetIpInterfaceEntry.argtypes = [ctypes.POINTER(MIB_IPINTERFACE_ROW)]


def set_adapter_mtu(adapter_handle: HANDLE, mtu: int) -> None:
    luid = DWORD()
    if not wintun.WintunGetAdapterLUID(adapter_handle, byref(luid)):
        raise Exception("Failed to get adapter LUID.")

    row = MIB_IPINTERFACE_ROW()
    ctypes.memset(byref(row), 0, ctypes.sizeof(row))  # Zero-initialize the structure
    row.InterfaceLuid = luid.value  # Assuming interface_luid is already a ULARGE_INTEGER
    row.Family = 2  # Assuming IPv4; for IPv6, use AF_INET6 or 23

    # Attempt to get the current interface entry to ensure all other fields are correctly populated
    result = iphlpapi.GetIpInterfaceEntry(byref(row))
    if result != 0:
        print(f"Failed to get IP interface entry, error code: {result}")
        return False

    row.Mtu = mtu  # Set the new MTU value

    # Attempt to set the modified interface entry
    result = iphlpapi.SetIpInterfaceEntry(byref(row))
    if result != 0:
        raise Exception(f"Failed to set adapter MTU, error code: {result}")


# Example usage:
if __name__ == '__main__':
    # Define or obtain necessary GUIDs and names
    adapter_name = "MyVirtualAdapter"
    tunnel_type_guid = (ctypes.c_ubyte * 16)(*bytearray.fromhex('1122'))
    requested_guid = (ctypes.c_ubyte * 16)(*bytearray.fromhex('1122'))
    allocated_guid = (ctypes.c_ubyte * 16)()  # Empty GUID, to be filled by the function
    last_error = DWORD()

    # Create an adapter
    adapter_handle = wintun.WintunCreateAdapter(adapter_name, ctypes.byref(tunnel_type_guid), ctypes.byref(requested_guid),
                                                ctypes.byref(allocated_guid), ctypes.byref(last_error))

    if adapter_handle:
        print("Adapter created successfully.")

        set_adapter_mtu(adapter_handle, 1500)

        # Delete the adapter when done
        success = wintun.WintunCloseAdapter(adapter_handle)
        if success:
            print("Adapter deleted successfully.")
        else:
            print(f"Failed to delete adapter. Last error: {last_error.value}")
    else:
        print(f"Failed to create adapter. Last error: {last_error.value}")

    session_handle = wintun.WintunStartSession(adapter_handle, (ctypes.c_ulong(0x400000)))













import pywintunx_pmd3

def log(level: int, timestamp: int, message: str):
  pass

pywintunx_pmd3.set_logger(log)
pywintunx_pmd3.install_wetest_driver()
pywintunx_pmd3.uninstall_wetest_driver()

tun_dev = pywintunx_pmd3.TunTapDevice()
# Avaliable constructor include
# or TunTapDevice(name='XX')
# or TunTapDevice(name='XX', type='xxx')
# or TunTapDevice(name='XX', type='xxx', guid='xxxs')
# or TunTapDevice(name='XX', type='xxx', proto_aware=True)
# tundev.name, readonly property
tun_dev.ring_capacity = 8*1024*1024
tun_dev.mtu4 = 1460             # set ipv4 subinterface mtu
tun_dev.mtu = 1452              # set ipv6 subinterface mtu
tun_dev.addr4 = '10.2.3.4:8899'       # set ipv4 subinterface address
#tun_dev.addr4 = '77.37.63.119:9000'       # set ipv4 subinterface address
#tun_dev.addr = 'ffee:aadf:8877:2'# set ipv6 subinterface mtu
tun_dev.up()

while True:
    packet = tun_dev.read() # receive a packet
    print(packet)
    tun_dev.wait_read_event()

    if packet:
        tun_dev.write(packet)#(b'\x00') # send a packet..

tun_dev.down()

...
tun_dev.close()
