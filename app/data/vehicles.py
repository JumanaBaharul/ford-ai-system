"""
Synthetic Ford Vehicle Dataset
Contains vehicle specs, service schedules, and owner manual content.
"""

VEHICLES = [
    {
        "id": "f150_2023",
        "model": "Ford F-150",
        "year": 2023,
        "category": "pickup truck",
        "engine": "3.5L EcoBoost V6 Twin-Turbocharged, 400 hp, 500 lb-ft torque",
        "transmission": "10-speed SelectShift Automatic",
        "fuel_type": "Gasoline (E85 FlexFuel compatible)",
        "fuel_economy": "20 MPG city / 26 MPG highway",
        "seating_capacity": 5,
        "towing_capacity": "14,000 lbs (max)",
        "payload_capacity": "2,238 lbs",
        "drivetrain": "4WD / RWD selectable",
        "safety_features": [
            "Pre-Collision Assist with Automatic Emergency Braking",
            "Lane-Keeping System",
            "Blind Spot Information System",
            "Rear View Camera",
            "Pro Trailer Backup Assist",
            "360-Degree Camera",
            "Ford Co-Pilot360 Suite"
        ],
        "tech_features": [
            "SYNC 4 Infotainment (12-inch touchscreen)",
            "Built-in 4G LTE Wi-Fi hotspot",
            "Apple CarPlay / Android Auto",
            "Available onboard generator (7.2kW Pro Power Onboard)",
            "BlueCruise hands-free highway driving"
        ],
        "dimensions": {
            "length": "231.7 inches (SuperCrew)",
            "width": "79.9 inches",
            "height": "75.5 inches",
            "wheelbase": "145 inches"
        },
        "price_range": "$36,000 – $74,000",
        "use_case": "Heavy towing, hauling, work truck, family pickup",
        "pros": ["Best-in-class towing", "Powerful engine options", "Spacious cab", "High payload"],
        "cons": ["Lower fuel economy", "Large size can be hard to park"]
    },
    {
        "id": "mustang_2023",
        "model": "Ford Mustang",
        "year": 2023,
        "category": "sports car / coupe",
        "engine": "5.0L Ti-VCT V8, 450 hp, 410 lb-ft torque (GT trim)",
        "transmission": "6-speed manual or 10-speed automatic",
        "fuel_type": "Gasoline (Premium recommended for V8)",
        "fuel_economy": "15 MPG city / 24 MPG highway (V8)",
        "seating_capacity": 4,
        "towing_capacity": "Not rated for towing",
        "payload_capacity": "N/A",
        "drivetrain": "RWD",
        "safety_features": [
            "Pre-Collision Assist",
            "Blind Spot Information System",
            "Rear Cross-Traffic Alert",
            "Lane-Keeping Alert",
            "Rear View Camera"
        ],
        "tech_features": [
            "SYNC 4 (12-inch touchscreen)",
            "Apple CarPlay / Android Auto",
            "Bang & Olufsen Premium Audio",
            "Track Apps (lap timer, 0-60 timer)",
            "Launch Control"
        ],
        "dimensions": {
            "length": "188.5 inches",
            "width": "75.4 inches",
            "height": "54.4 inches",
            "wheelbase": "107.1 inches"
        },
        "price_range": "$31,000 – $60,000",
        "use_case": "Performance driving, weekend car, enthusiast, sports car",
        "pros": ["Iconic styling", "Thrilling V8 performance", "Manual transmission available", "Track-ready"],
        "cons": ["Rear seat is cramped", "Poor fuel economy", "No towing capability"]
    },
    {
        "id": "explorer_2023",
        "model": "Ford Explorer",
        "year": 2023,
        "category": "midsize SUV",
        "engine": "2.3L EcoBoost Inline-4, 300 hp, 310 lb-ft torque",
        "transmission": "10-speed SelectShift Automatic",
        "fuel_type": "Gasoline",
        "fuel_economy": "21 MPG city / 28 MPG highway",
        "seating_capacity": 7,
        "towing_capacity": "5,600 lbs",
        "payload_capacity": "1,520 lbs",
        "drivetrain": "RWD / AWD selectable",
        "safety_features": [
            "Ford Co-Pilot360 (standard)",
            "Pre-Collision Assist with Automatic Emergency Braking",
            "Blind Spot Information System",
            "Rear Cross-Traffic Alert",
            "Lane-Keeping System",
            "Adaptive Cruise Control with Stop-and-Go",
            "Evasive Steering Assist",
            "Post-Collision Braking"
        ],
        "tech_features": [
            "SYNC 4 (10.1-inch portrait touchscreen)",
            "Apple CarPlay / Android Auto",
            "Available 360-degree camera",
            "Rear-Seat Entertainment System",
            "Wi-Fi hotspot"
        ],
        "dimensions": {
            "length": "198.8 inches",
            "width": "78.9 inches",
            "height": "70.1 inches",
            "wheelbase": "119.1 inches"
        },
        "price_range": "$38,000 – $60,000",
        "use_case": "Family road trips, 3-row family hauler, suburban driving",
        "pros": ["7-seat capacity", "Strong towing for class", "Spacious cargo", "Smooth ride"],
        "cons": ["Third row is tight for adults", "Base engine can feel strained when loaded"]
    },
    {
        "id": "escape_2023",
        "model": "Ford Escape",
        "year": 2023,
        "category": "compact SUV / crossover",
        "engine": "1.5L EcoBoost Inline-3, 181 hp, 190 lb-ft torque",
        "transmission": "8-speed automatic",
        "fuel_type": "Gasoline / Plug-in Hybrid available",
        "fuel_economy": "28 MPG city / 34 MPG highway (gasoline)",
        "seating_capacity": 5,
        "towing_capacity": "2,000 lbs",
        "payload_capacity": "850 lbs",
        "drivetrain": "FWD / AWD selectable",
        "safety_features": [
            "Ford Co-Pilot360 (standard)",
            "Pre-Collision Assist",
            "Blind Spot Information System",
            "Lane Centering",
            "Auto High-Beam Headlamps",
            "Rear View Camera"
        ],
        "tech_features": [
            "SYNC 4 (13.2-inch touchscreen)",
            "Apple CarPlay / Android Auto",
            "Wireless charging pad",
            "Available plug-in hybrid (PHEV) with 37-mile EV range"
        ],
        "dimensions": {
            "length": "180.5 inches",
            "width": "74.1 inches",
            "height": "66.1 inches",
            "wheelbase": "106.7 inches"
        },
        "price_range": "$28,000 – $42,000",
        "use_case": "City driving, commuting, small families, fuel efficiency",
        "pros": ["Excellent fuel economy", "Easy to park", "Modern tech", "PHEV option"],
        "cons": ["Limited cargo space vs larger SUVs", "Modest towing", "Small third-row not available"]
    },
    {
        "id": "ranger_2023",
        "model": "Ford Ranger",
        "year": 2023,
        "category": "midsize pickup truck",
        "engine": "2.3L EcoBoost Inline-4, 270 hp, 310 lb-ft torque",
        "transmission": "10-speed automatic",
        "fuel_type": "Gasoline",
        "fuel_economy": "21 MPG city / 26 MPG highway",
        "seating_capacity": 5,
        "towing_capacity": "7,500 lbs",
        "payload_capacity": "1,860 lbs",
        "drivetrain": "RWD / 4WD selectable",
        "safety_features": [
            "Pre-Collision Assist with Automatic Emergency Braking",
            "Blind Spot Information System",
            "Rear Cross-Traffic Alert",
            "Lane-Keeping System",
            "Rear View Camera",
            "Trail Control (off-road cruise control)"
        ],
        "tech_features": [
            "SYNC 4 (12-inch touchscreen)",
            "Apple CarPlay / Android Auto",
            "FordPass Connect (remote start, lock/unlock)",
            "Off-Road mode with terrain management"
        ],
        "dimensions": {
            "length": "210.8 inches (SuperCrew)",
            "width": "73.3 inches",
            "height": "70.9 inches",
            "wheelbase": "127 inches"
        },
        "price_range": "$32,000 – $48,000",
        "use_case": "Midsize towing, off-roading, weekend adventures, work/play balance",
        "pros": ["More maneuverable than F-150", "Capable off-road", "Good towing", "Comfortable ride"],
        "cons": ["Less powerful than F-150", "Smaller bed than full-size trucks"]
    }
]

SERVICE_DATA = [
    {
        "model": "Ford F-150",
        "year": 2023,
        "oil_change_interval": "Every 7,500 miles or 6 months (synthetic oil); every 5,000 miles (conventional)",
        "tire_rotation": "Every 7,500 miles or 6 months",
        "brake_inspection": "Every 20,000 miles or annually; replace pads when under 2mm",
        "air_filter": "Every 30,000 miles or 3 years",
        "spark_plugs": "Every 100,000 miles (Motorcraft iridium plugs)",
        "coolant_flush": "Every 100,000 miles or 10 years",
        "transmission_service": "Every 150,000 miles under normal use; inspect every 30,000",
        "battery_check": "Every 3–5 years; check terminals annually",
        "warranty": {
            "basic": "3 years / 36,000 miles bumper-to-bumper",
            "powertrain": "5 years / 60,000 miles",
            "roadside": "5 years / 60,000 miles",
            "corrosion": "5 years / unlimited miles"
        },
        "service_interval_table": "Oil (7.5k), Tires (7.5k), Brakes (20k), Air Filter (30k), Plugs (100k)"
    },
    {
        "model": "Ford Mustang",
        "year": 2023,
        "oil_change_interval": "Every 7,500 miles or 6 months (V8); every 10,000 miles (EcoBoost with full synthetic)",
        "tire_rotation": "Every 7,500 miles (check for uneven wear more frequently with performance tires)",
        "brake_inspection": "Every 15,000 miles (high-performance brakes wear faster under spirited driving)",
        "air_filter": "Every 25,000 miles (more often in dusty/track conditions)",
        "spark_plugs": "Every 60,000 miles (V8); 100,000 miles (EcoBoost)",
        "coolant_flush": "Every 100,000 miles",
        "transmission_service": "Manual: inspect clutch every 60,000 miles; Auto: 150,000 miles normal use",
        "battery_check": "Every 3–5 years",
        "warranty": {
            "basic": "3 years / 36,000 miles",
            "powertrain": "5 years / 60,000 miles",
            "roadside": "5 years / 60,000 miles",
            "corrosion": "5 years / unlimited miles"
        },
        "service_interval_table": "Oil (7.5k/10k), Tires (7.5k), Brakes (15k), Air Filter (25k), Plugs (60k-100k)"
    },
    {
        "model": "Ford Explorer",
        "year": 2023,
        "oil_change_interval": "Every 10,000 miles or 12 months (full synthetic oil)",
        "tire_rotation": "Every 7,500 miles",
        "brake_inspection": "Every 20,000 miles or annually",
        "air_filter": "Every 30,000 miles",
        "spark_plugs": "Every 100,000 miles",
        "coolant_flush": "Every 100,000 miles",
        "transmission_service": "Inspect every 30,000 miles; fluid change at 150,000 under normal use",
        "battery_check": "Every 3–5 years",
        "warranty": {
            "basic": "3 years / 36,000 miles",
            "powertrain": "5 years / 60,000 miles",
            "roadside": "5 years / 60,000 miles",
            "corrosion": "5 years / unlimited miles"
        },
        "service_interval_table": "Oil (10k), Tires (7.5k), Brakes (20k), Air Filter (30k), Plugs (100k)"
    },
    {
        "model": "Ford Escape",
        "year": 2023,
        "oil_change_interval": "Every 10,000 miles or 12 months (synthetic); PHEV: every 12 months regardless of mileage",
        "tire_rotation": "Every 7,500 miles",
        "brake_inspection": "Every 20,000 miles (PHEV brakes last longer due to regenerative braking)",
        "air_filter": "Every 30,000 miles",
        "spark_plugs": "Every 100,000 miles",
        "coolant_flush": "Every 100,000 miles",
        "transmission_service": "Every 150,000 miles under normal conditions",
        "battery_check": "12V battery: 3–5 years; PHEV high-voltage battery: covered by 10yr/150k warranty",
        "warranty": {
            "basic": "3 years / 36,000 miles",
            "powertrain": "5 years / 60,000 miles",
            "roadside": "5 years / 60,000 miles",
            "corrosion": "5 years / unlimited miles",
            "hybrid_battery": "10 years / 150,000 miles (PHEV only)"
        },
        "service_interval_table": "Oil (10k/12mo), Tires (7.5k), Brakes (20k), Air Filter (30k), Plugs (100k)"
    },
    {
        "model": "Ford Ranger",
        "year": 2023,
        "oil_change_interval": "Every 7,500 miles or 6 months (synthetic)",
        "tire_rotation": "Every 7,500 miles",
        "brake_inspection": "Every 20,000 miles or annually",
        "air_filter": "Every 30,000 miles (more often in off-road/dusty use)",
        "spark_plugs": "Every 100,000 miles",
        "coolant_flush": "Every 100,000 miles",
        "transmission_service": "Every 150,000 miles normal use; inspect every 30,000",
        "battery_check": "Every 3–5 years",
        "warranty": {
            "basic": "3 years / 36,000 miles",
            "powertrain": "5 years / 60,000 miles",
            "roadside": "5 years / 60,000 miles",
            "corrosion": "5 years / unlimited miles"
        },
        "service_interval_table": "Oil (7.5k), Tires (7.5k), Brakes (20k), Air Filter (30k), Plugs (100k)"
    }
]

OWNER_MANUAL_CHUNKS = [
    {
        "id": "warn_001",
        "title": "Check Engine Light (Solid)",
        "category": "dashboard_warning",
        "content": "A solid check engine light indicates the engine management system has detected a fault. Common causes include a loose or faulty fuel cap, oxygen sensor failure, catalytic converter issue, or spark plug misfires. The vehicle is generally safe to drive but should be inspected by a Ford-certified technician within 1–2 days. Do not ignore this warning for more than a week as it may worsen engine damage."
    },
    {
        "id": "warn_002",
        "title": "Check Engine Light (Flashing/Blinking)",
        "category": "dashboard_warning",
        "content": "A flashing check engine light indicates a severe engine misfire is occurring and raw fuel is being dumped into the catalytic converter, which can cause permanent damage within minutes. STOP DRIVING IMMEDIATELY in a safe location. Do not continue driving with a flashing check engine light. Call roadside assistance or a tow truck. This is a critical safety warning."
    },
    {
        "id": "warn_003",
        "title": "Oil Pressure Warning Light",
        "category": "dashboard_warning",
        "content": "The oil pressure warning light (oil can icon) means oil pressure has dropped dangerously low. STOP THE ENGINE IMMEDIATELY and do not restart. Low oil pressure can cause catastrophic engine damage within seconds of running. Check oil level using the dipstick. If oil level is normal, do not restart — call for service. If oil is low, add the correct grade oil and recheck. If light remains on after topping up, have the vehicle towed."
    },
    {
        "id": "warn_004",
        "title": "Battery / Charging System Warning",
        "category": "dashboard_warning",
        "content": "The battery warning light (battery icon) indicates the charging system is not working properly. The alternator may have failed or the battery connection is loose. The vehicle will continue running on battery power only, but the battery will deplete quickly (typically 20–30 minutes). Turn off all non-essential electrical loads (A/C, radio, heated seats). Drive directly to a service location or call for assistance. Do not turn off the engine as it may not restart."
    },
    {
        "id": "warn_005",
        "title": "Tire Pressure Monitor (TPMS) Warning",
        "category": "dashboard_warning",
        "content": "The TPMS light (exclamation point in tire icon) means one or more tires are significantly under-inflated (25% or more below recommended pressure). Check all four tires and inflate to the recommended PSI shown on the door jamb sticker (typically 35–38 PSI for most Ford models). Under-inflated tires reduce fuel economy, handling, and can cause blowouts at highway speeds. If the TPMS light blinks for 60–90 seconds then stays solid, the TPMS sensor itself may need service."
    },
    {
        "id": "warn_006",
        "title": "Coolant Temperature Warning",
        "category": "dashboard_warning",
        "content": "The coolant temperature warning (thermometer in water icon) means the engine is overheating. Pull over safely and turn off the engine immediately. Do NOT open the hood or coolant cap while the engine is hot — steam and hot coolant can cause serious burns. Wait at least 30 minutes for the engine to cool. Check coolant level in the overflow reservoir (never the radiator cap when hot). If coolant is low, add pre-mixed Ford-approved coolant. If the problem persists, have the vehicle towed — driving an overheated engine causes severe damage."
    },
    {
        "id": "warn_007",
        "title": "Brake Warning Light",
        "category": "dashboard_warning",
        "content": "The red brake warning light can indicate: (1) The parking brake is engaged — release it and the light should go off. (2) Brake fluid is low — check the reservoir under the hood and top up with DOT 4 fluid. Low brake fluid often indicates worn brake pads or a leak. (3) A brake system fault — if the light stays on after checking the above, have the vehicle inspected immediately. Do not drive with a brake fault. A yellow brake light typically indicates the ABS system has a fault."
    },
    {
        "id": "maint_001",
        "title": "Oil Change Reminder",
        "category": "maintenance_reminder",
        "content": "Ford vehicles use the Intelligent Oil-Life Monitor (IOLM) system which calculates oil life based on driving conditions, mileage, and engine stress. When the Oil Change Required message appears in the instrument cluster, service should be performed within 500 miles. To reset the oil life monitor after service: Press the OK button on the steering wheel until Oil Life appears, then hold OK for 2 seconds until 100% is displayed. Always use Ford-recommended oil grade (check door jamb or owner manual for your specific model)."
    },
    {
        "id": "maint_002",
        "title": "Tire Rotation and Inspection",
        "category": "maintenance_reminder",
        "content": "Tires should be rotated every 7,500 miles or 6 months (whichever comes first) to ensure even tread wear. During rotation, inspect tires for: uneven wear patterns (indicates alignment or suspension issues), sidewall cracks or bulges, tread depth below 2/32 inch (replace immediately), and embedded nails or objects. Maintain tire pressure as shown on the door jamb label. Properly inflated and rotated tires improve fuel economy by up to 3% and extend tire life by up to 20,000 miles."
    },
    {
        "id": "maint_003",
        "title": "Air Filter Inspection",
        "category": "maintenance_reminder",
        "content": "The engine air filter should be inspected every 15,000 miles and replaced every 30,000 miles (more frequently in dusty environments). A clogged air filter reduces engine performance, increases fuel consumption by up to 10%, and can cause rough idling. The cabin air filter (for HVAC) should also be replaced every 15,000–25,000 miles to maintain air quality and A/C efficiency inside the vehicle."
    },
    {
        "id": "trouble_001",
        "title": "Engine Won't Start – No Click",
        "category": "troubleshooting",
        "content": "If you turn the key or press the start button and hear nothing: (1) Ensure the vehicle is in Park (automatic) or Neutral with clutch pressed (manual). (2) Check that the key fob battery is not dead — try holding the fob against the start button. (3) Check for a dead 12V battery — look for dim interior lights. (4) Inspect battery terminals for corrosion (white/blue buildup). (5) Try jump-starting with a Ford-compatible jump pack or jumper cables. If none of these work, contact roadside assistance."
    },
    {
        "id": "trouble_002",
        "title": "Engine Cranks But Won't Start",
        "category": "troubleshooting",
        "content": "If the engine turns over but won't fire: (1) Check fuel level — the gauge may be inaccurate. (2) If the vehicle ran out of fuel, you may need to cycle the ignition 5–6 times to re-prime the fuel system. (3) Check for a theft indicator light — if the anti-theft system is engaged, the engine will crank but not start. Re-authenticate with the correct key fob. (4) In cold weather, the engine may need a longer cranking period. (5) If the issue persists, a failed fuel pump, clogged fuel filter, or failed crankshaft position sensor may be the cause — have the vehicle inspected."
    },
    {
        "id": "trouble_003",
        "title": "Rough Idle or Shaking",
        "category": "troubleshooting",
        "content": "A rough idle or vibration at idle typically indicates: (1) Spark plug fouling or failure — replace spark plugs as per service schedule. (2) Dirty fuel injectors — use Ford-recommended fuel injector cleaner or have professional cleaning performed. (3) Vacuum leak in intake system — listen for a hissing sound under the hood. (4) Mass airflow sensor contamination — clean with MAF sensor cleaner spray. (5) Carbon buildup in direct-injection engines is common after 50,000+ miles. Professional intake cleaning recommended."
    },
    {
        "id": "trouble_004",
        "title": "Transmission Shudder or Hesitation",
        "category": "troubleshooting",
        "content": "Ford's 10-speed automatic transmission may exhibit shudder or hesitation in certain conditions: (1) Low transmission fluid — check level with the vehicle warm and running in Park. (2) Contaminated fluid (dark color or burnt smell) — transmission fluid flush required. (3) Torque converter shudder — Ford has released TSBs (Technical Service Bulletins) for certain models; dealer software updates may resolve this. (4) Cold weather operation — allow the transmission to warm up for 1–2 minutes before driving aggressively. If shudder persists above 50°F, have the dealer inspect."
    },
    {
        "id": "trouble_005",
        "title": "A/C Not Blowing Cold Air",
        "category": "troubleshooting",
        "content": "If the A/C is running but air is not cold: (1) Ensure A/C is turned ON (not just the fan). (2) Check if the cabin air filter is clogged — a blocked filter restricts airflow significantly. (3) The A/C refrigerant may be low — this requires a professional recharge at a service center. (4) Check if the A/C compressor clutch engages when A/C is on (you should hear a click). (5) In extreme heat, park in shade and recirculate interior air to help the A/C cope. (6) If air is blowing but only slightly cool, a refrigerant leak or failed compressor likely requires dealer service."
    }
]
