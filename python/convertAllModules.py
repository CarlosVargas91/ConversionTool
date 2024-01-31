from collections import namedtuple # To build structure arrays

import utilities
from convertModule import convertModule

import os


# Module structure
Module = namedtuple("Module", ["name", "abbreviation"])

# Define modules or read from directory
modules = [
    # Module('ADCDriver', 'Adc'),
    # Module('BSWGeneral', 'BSW'),
    # Module('BSWModeManager', 'BswM'),
    # Module('BSWMulticoreLibrary', 'Bmc'),
    # Module('BulkNvDataManager', 'BndM'),
    # Module('BusMirroring', 'Mirror'),
    # Module('CANDriver', 'Can'),
    # Module('CANInterface', 'CanIf'),
    # Module('CANNetworkManagement', 'CanNm'),
    # Module('CANStateManager', 'CanSM'),
    # Module('CANTransceiverDriver', 'CanTrcv'),
    # Module('CANTransportLayer', 'CanTp'),
    # Module('CANXLDriver', 'CanXL'),
    # Module('CANXLTransceiverDriver', 'CanXLTrcv'),
    # Module('CellularV2XDriver', 'CV2x'),
    # Module('ChineseV2XManagement', 'CnV2xM'),
    # Module('ChineseV2XMessage', 'CnV2xMsg'),
    # Module('ChineseV2XNetwork', 'CnV2xNet'),
    # Module('ChineseV2XSecurity', 'CnV2xSec'),
    # Module('ClassicPlatformARTI', 'Arti'),
    # Module('ClassicPlatformDataDistributionService', 'Dds'),
    # Module('COM', 'Com'),
    # Module('COMBasedTransformer', 'ComXf'),
    # Module('COMManager', 'ComM'),
    # Module('CommunicationStackTypes', 'Comtype'),
    # Module('CoreTest', 'CorTst'),
    # Module('CRCLibrary', 'Crc'),
    # Module('CryptoDriver', 'Cry'),
    # Module('CryptoInterface', 'CryIf'),
    # Module('CryptoServiceManager', 'Csm'),
    # Module('DefaultErrorTracer', 'Det'),
    # Module('DiagnosticCommunicationManager', 'Dcm'),
    # Module('DiagnosticEventManager', 'Dem'),
    # Module('DiagnosticLogAndTrace', 'Dlt'),
    # Module('DiagnosticOverIP', 'DoIP'),
    # Module('DIODriver', 'Dio'),
    # Module('E2ELibrary', 'E2E'),
    # Module('E2ETransformer', 'E2EXf'),
    # Module('ECUStateManager', 'EcuM'),
    # Module('EEPROMAbstraction', 'Ea'),
    # Module('EEPROMDriver', 'Eep'),
    # Module('EFXLibrary', 'Efx'),
    # Module('EthernetDriver', 'Eth'),
    # Module('EthernetInterface', 'EthIf'),
    # Module('EthernetStateManager', 'EthSM'),
    # Module('EthernetSwitchDriver', 'EthSwt'),
    # Module('EthernetTransceiverDriver', 'EthTrcv'),
    # Module('FlashDriver', 'Fls'),
    # Module('FlashEEPROMEmulation', 'Fee'),
    # Module('FlashTest', 'FlsTst'),
    # Module('FlexRayARTransportLayer', 'FrArTp'),
    # Module('FlexRayDriver', 'Fr'),
    # Module('FlexRayInterface', 'FrIf'),
    # Module('FlexRayISOTransportLayer', 'FrTp'),
    # Module('FlexRayNetworkManagement', 'FrNm'),
    # Module('FlexRayStateManager', 'FrSM'),
    # Module('FlexRayTransceiverDriver', 'FrTrcv'),
    # Module('FunctionInhibitionManager', 'Fim'),
    # Module('GPTDriver', 'Gpt'),
    # Module('HWTestManager', 'HTMSS'),
    # Module('ICUDriver', 'Icu'),
    # Module('IFLLibrary', 'Ifl'),
    # Module('IFXLibrary', 'Ifx'),
    # Module('IntrusionDetectionSystemManager', 'IdsM'),
    # Module('IOHardwareAbstraction', 'IoHwAb'),
    # Module('IPDUMultiplexer', 'IpduM'),
    # Module('KeyManager', 'KeyM'),
    # Module('LargeDataCOM', 'LDCOM'),
    # Module('LINDriver', 'Lin'),
    # Module('LINInterface', 'LinIf'),
    # Module('LINStateManager', 'LinSM'),
    # Module('LINTransceiverDriver', 'LinTrcv'),
    # Module('MACsecKeyAgreement', 'Mka'),
    # Module('MCUDriver', 'Mcu'),
    # Module('MemoryAbstractionInterface', 'MemIf'),
    # Module('MemoryAccess', 'MemAcc'),
    # Module('MemoryDriver', 'Mem'),
    # Module('MemoryMapping', 'MemMap'),
    # Module('MFLLibrary', 'Mfl'),
    # Module('MFXLibrary', 'Mfx'),
    # Module('NetworkManagementInterface', 'Nm'),
    # Module('NVRAMManager', 'NvM'),
    # Module('OCUDriver', 'Ocu'),
    # Module('OS', 'Os'),
    # Module('PDURouter', 'PduR'),
    # Module('PlatformTypes', 'Platform'),
    # Module('PortDriver', 'Port'),
    # Module('PWMDriver', 'Pwm'),
    # Module('RAMTest', 'RamTst'),
    # Module('RTE', 'Rte'),
    # Module('SAEJ1939DiagnosticCommunicationManager', 'J1939Dcm'),
    # Module('SAEJ1939NetworkManagement', 'XXXXXXXXXXXXXXXX'), Just in R19
    # Module('SAEJ1939RequestManager', 'J1939Rm'),
    # Module('SAEJ1939TransportLayer', 'J1939Tp'),
    # Module('SecureOnboardCommunication', 'SecOC'),
    # Module('ServiceDiscovery', 'SD'),
    # Module('SocketAdaptor', 'SoAd'),
    # Module('SoftwareClusterConnection', 'SwCluC'),
    # Module('SOMEIPTransformer', 'SomeIpXf'),
    # Module('SOMEIPTransportProtocol', 'SomeIpTp'),
    # Module('SPIHandlerDriver', 'Spi'),
    # Module('StandardTypes', 'Std'),
    # Module('SynchronizedTimeBaseManager', 'StbM'),
    # Module('TcpIp', 'TcpIp'), # Has problems
    # Module('TimeService', 'Tm'),
    # Module('TimeSyncOverCAN', 'CanTSyn'),
    # Module('TimeSyncOverEthernet', 'EthTSyn'),
    # Module('TimeSyncOverFlexRay', 'FrTSyn'),
    # Module('TTCANDriver', 'TtCan'),
    # Module('TTCANInterface', 'TtCanIf'),
    # Module('UDPNetworkManagement', 'UdpNm'),
    # Module('V2XBasicTransport', 'V2xBtp'),
    # Module('V2XDataManager', 'V2xDM'),
    # Module('V2XFacilities', 'V2xFac'),
    # Module('V2XGeoNetworking', 'V2xGn'),
    # Module('V2XManagement', 'V2xM'),
    # Module('WatchdogDriver', 'Wdg'),
    # Module('WatchdogInterface', 'WdgIf'),
    # Module('WatchdogManager', 'WdgM'),
    # Module('WirelessEthernetDriver', 'WEth'),
    # Module('WirelessEthernetTransceiverDriver', 'WEthTrcv'),
    # Module('XCP', 'Xcp'),
]

# Loop through all modules
for curModule in modules:
# curModule = modules[1]
# if 1:
    # Construct filename
    fileName = 'AUTOSAR_SWS_' + curModule.name

    # Print starting header
    utilities.printHeader('[' + curModule.abbreviation + '] Start processing ' + fileName + '.pdf')

    # Call external functions
    convertModule(curModule.name, curModule.abbreviation, fileName)

    # Print ending header
    # utilities.printHeader('[' + curModule.abbreviation + '] Done processing ' + fileName + '.pdf')

    # Extra whitespace
    # print()
    utilities.printInfo(' End of process ')


# Helper to construct module list:
# dir_list = os.listdir('..')

# for dire in dir_list:
#     temp_str = dire.replace('.pdf', '').replace('AUTOSAR_SWS_', '')
#     print("    Module('" + temp_str + "', 'XXXXXXXXXXXXXXXX'),")