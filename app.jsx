import React, { useState, useEffect, useCallback } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, doc, onSnapshot } from 'firebase/firestore';
import { RefreshCw, Leaf, Thermometer, Droplets, FlaskConical, Wifi } from 'lucide-react';

// --- Global Firebase Configuration (MUST BE USED) ---
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

// --- Prediction Logic (Simulating Random Forest Output) ---
// This logic runs in the browser using the latest data from the ESP32.
const predictCrop = (N, P, K, temp, humidity, ph) => {
    if (N === null) return "Waiting for ESP32 Data...";
    
    // Simple checks for data validation
    if (!(5.5 <= ph <= 7.5) || !(15 <= temp <= 35) || !(40 <= humidity <= 90)) {
        return "Environmental conditions are outside optimal range. Consider corrective action.";
    }

    let crop = "General Field Crop (Wheat/Maize)";

    // --- Decision Tree Simulation based on common agricultural rules (Random Forest output) ---
    if (ph < 6.0) { // Acidic Soil
        if (N < 40 && K > 50) {
            crop = "Coffee (Acid-loving, high Potassium)";
        } else if (temp < 20) {
            crop = "Potatoes or Berries";
        }
    } else if (ph > 7.0) { // Alkaline Soil
        if (P > 60 && temp > 28) {
            crop = "Cotton (Tolerates alkalinity, needs heat)";
        } else if (K > 80) {
            crop = "Grapes or Barley";
        }
    } else { // Neutral Soil (6.0 - 7.0)
        if (temp > 30 && humidity > 80) {
            crop = "Rice (High heat and humidity)";
        } else if (N > 80 && P > 50) {
            crop = "Sugarcane or High-Yield Maize";
        }
    }

    return crop;
};


// --- React Component ---
const App = () => {
    const [soilData, setSoilData] = useState({ N: null, P: null, K: null, ph: null, temperature: null, humidity: null, timestamp: null });
    const [db, setDb] = useState(null);
    const [auth, setAuth] = useState(null);
    const [userId, setUserId] = useState(null);
    const [connectionStatus, setConnectionStatus] = useState('Initializing...');

    // 1. Firebase Initialization and Authentication
    useEffect(() => {
        try {
            const app = initializeApp(firebaseConfig);
            const firestore = getFirestore(app);
            const firebaseAuth = getAuth(app);
            
            setDb(firestore);
            setAuth(firebaseAuth);

            const authenticate = async () => {
                if (initialAuthToken) {
                    await signInWithCustomToken(firebaseAuth, initialAuthToken);
                } else {
                    await signInAnonymously(firebaseAuth);
                }
                
                firebaseAuth.onAuthStateChanged(user => {
                    if (user) {
                        setUserId(user.uid);
                        setConnectionStatus('Authenticated. Waiting for sensor data...');
                    } else {
                        setConnectionStatus('Authentication Failed.');
                    }
                });
            };
            authenticate();
        } catch (error) {
            console.error("Firebase initialization failed:", error);
            setConnectionStatus(`Error: ${error.message}`);
        }
    }, []);

    // 2. Real-time Data Listener
    useEffect(() => {
        if (db && userId) {
            // Path: /artifacts/{appId}/public/data/soil_readings/{documentId}
            // We listen to a fixed document ID 'latest_reading' which the ESP32 updates.
            const docRef = doc(db, `artifacts/${appId}/public/data/soil_readings/latest_reading`);
            
            const unsubscribe = onSnapshot(docRef, (docSnapshot) => {
                if (docSnapshot.exists()) {
                    const data = docSnapshot.data();
                    console.log("New data received:", data);
                    setSoilData({
                        N: data.N,
                        P: data.P,
                        K: data.K,
                        ph: data.ph,
                        temperature: data.temperature,
                        humidity: data.humidity,
                        timestamp: data.timestamp ? new Date(data.timestamp.toDate()).toLocaleTimeString() : 'N/A',
                        deviceId: data.deviceId || 'Unknown',
                    });
                    setConnectionStatus('Live Data Stream Active');
                } else {
                    setConnectionStatus('Waiting for ESP32 to publish data to Firestore...');
                }
            }, (error) => {
                console.error("Firestore error:", error);
                setConnectionStatus(`Firestore Error: ${error.message}`);
            });

            // Cleanup listener on component unmount
            return () => unsubscribe();
        }
    }, [db, userId]);

    const { N, P, K, ph, temperature, humidity, timestamp, deviceId } = soilData;
    const prediction = predictCrop(N, P, K, temperature, humidity, ph);

    const dataAvailable = N !== null;

    // Helper Card Component
    const DataCard = ({ icon, label, value, unit, color }) => (
        <div className={`p-4 rounded-lg shadow-md flex items-center justify-between transition-transform duration-300 hover:scale-[1.02] ${color}`}>
            <div className="flex items-center space-x-3">
                {icon}
                <span className="text-sm font-medium">{label}</span>
            </div>
            <div className="text-2xl font-bold">
                {value !== null ? `${value}` : '---'}
                <span className="text-base font-normal ml-1">{unit}</span>
            </div>
        </div>
    );


    return (
        <div className="min-h-screen bg-gray-50 p-4 sm:p-8 font-sans">
            <header className="text-center mb-8">
                <h1 className="text-4xl font-extrabold text-green-700 flex items-center justify-center">
                    <Leaf className="w-8 h-8 mr-3 text-green-500" />
                    CropSense AI Dashboard
                </h1>
                <p className="text-sm text-gray-500 mt-2">
                    Real-time monitoring and Random Forest prediction from ESP32.
                </p>
            </header>

            {/* Connection Status & Metadata */}
            <div className="mb-8 p-4 bg-white rounded-lg shadow-xl border-t-4 border-green-500">
                <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center">
                        <Wifi className={`w-4 h-4 mr-2 ${dataAvailable ? 'text-green-500' : 'text-yellow-500'}`} />
                        <span>Status: {connectionStatus}</span>
                    </div>
                    <span>Last Update: <span className="font-semibold">{timestamp || 'N/A'}</span></span>
                    <span>Device ID: <span className="font-semibold text-xs">{deviceId}</span></span>
                </div>
            </div>

            <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                {/* 1. Prediction Panel */}
                <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-xl border-l-4 border-green-700">
                    <h2 className="text-2xl font-semibold mb-4 text-gray-700">
                        <RefreshCw className="inline w-5 h-5 mr-2 text-green-600 animate-spin" />
                        AI Prediction
                    </h2>
                    <div className="p-6 bg-green-50 rounded-lg border border-green-300">
                        <p className="text-lg font-medium text-gray-600 mb-2">Recommended Crop:</p>
                        <h3 className="text-4xl font-extrabold text-green-800">
                            {dataAvailable ? prediction : '...Awaiting Data...'}
                        </h3>
                        <p className="mt-4 text-sm text-gray-500">
                            *Prediction based on current soil parameters and simulated Random Forest rules.
                        </p>
                    </div>
                </div>

                {/* 2. Soil Parameter Data Cards */}
                <div className="lg:col-span-1 space-y-4">
                    <h2 className="text-2xl font-semibold text-gray-700">Soil Data</h2>
                    
                    <DataCard 
                        icon={<Leaf className="w-6 h-6 text-indigo-500" />}
                        label="Nitrogen (N)"
                        value={N}
                        unit="ppm"
                        color="bg-indigo-100"
                    />
                    <DataCard 
                        icon={<Leaf className="w-6 h-6 text-orange-500" />}
                        label="Phosphorus (P)"
                        value={P}
                        unit="ppm"
                        color="bg-orange-100"
                    />
                    <DataCard 
                        icon={<Leaf className="w-6 h-6 text-red-500" />}
                        label="Potassium (K)"
                        value={K}
                        unit="ppm"
                        color="bg-red-100"
                    />
                    <DataCard 
                        icon={<FlaskConical className="w-6 h-6 text-purple-500" />}
                        label="pH Level"
                        value={ph ? ph.toFixed(1) : null}
                        unit=""
                        color="bg-purple-100"
                    />
                </div>
            </main>

            {/* Environmental Data */}
            <div className="mt-8 p-6 bg-white rounded-lg shadow-xl">
                <h2 className="text-2xl font-semibold mb-4 text-gray-700">Environmental Readings</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <DataCard 
                        icon={<Thermometer className="w-6 h-6 text-red-600" />}
                        label="Temperature"
                        value={temperature ? temperature.toFixed(1) : null}
                        unit="°C"
                        color="bg-red-50"
                    />
                    <DataCard 
                        icon={<Droplets className="w-6 h-6 text-blue-600" />}
                        label="Humidity"
                        value={humidity ? humidity.toFixed(0) : null}
                        unit="%"
                        color="bg-blue-50"
                    />
                </div>
            </div>

        </div>
    );
};

export default App;