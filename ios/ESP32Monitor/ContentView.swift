import SwiftUI
import CoreBluetooth

struct ContentView: View {
    @StateObject private var esp32Manager = ESP32Manager()
    
    var body: some View {
        VStack {
            Text("ESP32 Monitor")
                .font(.title)
            
            // Connection Status
            Text(esp32Manager.connectionStatus)
                .foregroundColor(esp32Manager.isConnected ? .green : .red)
            
            // Sensor Data
            if esp32Manager.isConnected {
                VStack(alignment: .leading) {
                    Text("Air Temp: \(esp32Manager.airTemp, specifier: "%.1f")°C")
                    Text("Soil (10cm): \(esp32Manager.soilTemp10cm, specifier: "%.1f")°C")
                    Text("Soil (30cm): \(esp32Manager.soilTemp30cm, specifier: "%.1f")°C")
                    Text("Rain pH: \(esp32Manager.ph, specifier: "%.1f")")
                }
                .padding()
            }
            
            // Connection Buttons
            HStack {
                Button("Connect via BLE") {
                    esp32Manager.connectViaBLE()
                }
                .disabled(esp32Manager.isConnected)
                
                Button("Connect via WiFi") {
                    esp32Manager.connectViaWiFi()
                }
                .disabled(esp32Manager.isConnected)
                
                Button("Disconnect") {
                    esp32Manager.disconnect()
                }
                .disabled(!esp32Manager.isConnected)
            }
            .padding()
        }
    }
}

class ESP32Manager: NSObject, ObservableObject, CBCentralManagerDelegate {
    @Published var isConnected = false
    @Published var connectionStatus = "Disconnected"
    @Published var airTemp: Double = 0.0
    @Published var soilTemp10cm: Double = 0.0
    @Published var soilTemp30cm: Double = 0.0
    @Published var ph: Double = 7.0
    
    private var centralManager: CBCentralManager!
    private var connectedPeripheral: CBPeripheral?
    
    override init() {
        super.init()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }
    
    func connectViaBLE() {
        // TODO: Implement BLE connection to ESP32
        connectionStatus = "Scanning for ESP32..."
        // For now simulate connection
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.isConnected = true
            self.connectionStatus = "Connected via BLE"
            self.startMockDataUpdates()
        }
    }
    
    func connectViaWiFi() {
        // TODO: Implement WiFi connection to ESP32
        connectionStatus = "Connecting via WiFi..."
        // For now simulate connection
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.isConnected = true
            self.connectionStatus = "Connected via WiFi"
            self.startMockDataUpdates()
        }
    }
    
    func disconnect() {
        isConnected = false
        connectionStatus = "Disconnected"
        connectedPeripheral = nil
    }
    
    private func startMockDataUpdates() {
        Timer.scheduledTimer(withTimeInterval: 2, repeats: true) { _ in
            self.temperature = Double.random(in: 20...30)
            self.humidity = Double.random(in: 30...70)
            self.airQuality = Int.random(in: 300...600)
        }
    }
    
    // CBCentralManagerDelegate methods
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if central.state == .poweredOn {
            print("Bluetooth is ready")
        } else {
            print("Bluetooth not available")
        }
    }
}
