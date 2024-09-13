from random import sample
from fasthtml.common import *

app = FastHTML(hdrs=(picolink,))

vehicles = [
    {"name": "Tesla Model S 2022", "src": "https://pollinations.ai/p/Tesla%20Model%20S%202022?model=flux", "speed": 200},
    {"name": "Ford Mustang 1965", "src": "https://pollinations.ai/p/Ford%20Mustang%201965?model=flux", "speed": 145},
    {"name": "Porsche 911 Carrera 2022", "src": "https://pollinations.ai/p/Porsche%20911%20Carrera%202022?model=flux", "speed": 193},
    {"name": "Kawasaki Ninja H2R 2021", "src": "https://pollinations.ai/p/Kawasaki%20Ninja%20H2R%202021?model=flux", "speed": 240},
    {"name": "Yamaha SRX 120 Snowmobile 2022", "src": "https://pollinations.ai/p/Yamaha%20SRX%20120%20Snowmobile%202022?model=flux", "speed": 30},
    {"name": "Boeing 747 1989", "src": "https://pollinations.ai/p/Boeing%20747%201989?model=flux", "speed": 614},
    {"name": "Lamborghini Aventador 2021", "src": "https://pollinations.ai/p/Lamborghini%20Aventador%202021?model=flux", "speed": 217},
    {"name": "Harley-Davidson Roadster 2020", "src": "https://pollinations.ai/p/Harley-Davidson%20Roadster%202020?model=flux", "speed": 120},
    {"name": "Toyota Hilux 2020", "src": "https://pollinations.ai/p/Toyota%20Hilux%202020?model=flux", "speed": 105},
    {"name": "Chevrolet Corvette Stingray 2021", "src": "https://pollinations.ai/p/Chevrolet%20Corvette%20Stingray%202021?model=flux", "speed": 194},
    {"name": "Ferrari F8 Tributo 2021", "src": "https://pollinations.ai/p/Ferrari%20F8%20Tributo%202021?model=flux", "speed": 211},
    {"name": "Audi R8 2022", "src": "https://pollinations.ai/p/Audi%20R8%202022?model=flux", "speed": 205},
    {"name": "Bugatti Chiron 2020", "src": "https://pollinations.ai/p/Bugatti%20Chiron%202020?model=flux", "speed": 261},
    {"name": "McLaren Speedtail 2021", "src": "https://pollinations.ai/p/McLaren%20Speedtail%202021?model=flux", "speed": 250},
    {"name": "Ducati Panigale V4 2021", "src": "https://pollinations.ai/p/Ducati%20Panigale%20V4%202021?model=flux", "speed": 187},
    {"name": "Honda Civic Type R 2021", "src": "https://pollinations.ai/p/Honda%20Civic%20Type%20R%202021?model=flux", "speed": 169},
    {"name": "SpaceX Starship", "src": "https://pollinations.ai/p/SpaceX%20Starship?model=flux", "speed": 17000},
    {"name": "Ford F-150 Raptor 2021", "src": "https://pollinations.ai/p/Ford%20F-150%20Raptor%202021?model=flux", "speed": 107},
    {"name": "Tesla Cybertruck 2022", "src": "https://pollinations.ai/p/Tesla%20Cybertruck%202022?model=flux", "speed": 120},
    {"name": "Chrysler Pacifica 2021", "src": "https://pollinations.ai/p/Chrysler%20Pacifica%202021?model=flux", "speed": 112},
    {"name": "Cessna Skyhawk 172 2019", "src": "https://pollinations.ai/p/Cessna%20Skyhawk%20172%202019?model=flux", "speed": 140},
    {"name": "Lockheed SR-71 Blackbird 1966", "src": "https://pollinations.ai/p/Lockheed%20SR-71%20Blackbird%201966?model=flux", "speed": 2100},
    {"name": "Mercedes-Benz G-Class 2022", "src": "https://pollinations.ai/p/Mercedes-Benz%20G-Class%202022?model=flux", "speed": 130},
    {"name": "Mini Cooper SE 2021", "src": "https://pollinations.ai/p/Mini%20Cooper%20SE%202021?model=flux", "speed": 93},
    {"name": "Toyota Land Cruiser 2021", "src": "https://pollinations.ai/p/Toyota%20Land%20Cruiser%202021?model=flux", "speed": 129},
    {"name": "Hogwarts Express", "src": "https://pollinations.ai/p/Hogwarts%20Express?model=flux", "speed": 60},
    {"name": "Herbie the Love Bug", "src": "https://pollinations.ai/p/Herbie%20the%20Love%20Bug?model=flux", "speed": 90},
    {"name": "Millennium Falcon", "src": "https://pollinations.ai/p/Millennium%20Falcon?model=flux", "speed": 67000},
    {"name": "Apollo Lunar Module", "src": "https://pollinations.ai/p/Apollo%20Lunar%20Module?model=flux", "speed": 3408},
    {"name": "Jeep Wrangler Rubicon 2021", "src": "https://pollinations.ai/p/Jeep%20Wrangler%20Rubicon%202021?model=flux", "speed": 100},
    {"name": "Bumblebee (Transformers)", "src": "https://pollinations.ai/p/Bumblebee%20(Transformers)?model=flux", "speed": 198},
    {"name": "Enterprise NX-01", "src": "https://pollinations.ai/p/Enterprise%20NX-01?model=flux", "speed": 115000},
    {"name": "Delorean DMC-12 (Back to the Future)", "src": "https://pollinations.ai/p/Delorean%20DMC-12%20(Back%20to%20the%20Future)?model=flux", "speed": 88},
    {"name": "USS Enterprise (NCC-1701)", "src": "https://pollinations.ai/p/USS%20Enterprise%20(NCC-1701)?model=flux", "speed": 125000},
    {"name": "Marty's Hoverboard", "src": "https://pollinations.ai/p/Marty's%20Hoverboard?model=flux", "speed": 25},
    {"name": "AT-AT Walker", "src": "https://pollinations.ai/p/AT-AT%20Walker?model=flux", "speed": 37},
    {"name": "Batmobile (1989)", "src": "https://pollinations.ai/p/Batmobile%20(1989)?model=flux", "speed": 150},
    {"name": "X-wing Starfighter", "src": "https://pollinations.ai/p/X-wing%20Starfighter?model=flux", "speed": 1050},
    {"name": "General Lee (Dukes of Hazzard)", "src": "https://pollinations.ai/p/General%20Lee%20(Dukes%20of%20Hazzard)?model=flux", "speed": 125},
    {"name": "Optimus Prime", "src": "https://pollinations.ai/p/Optimus%20Prime?model=flux", "speed": 160},
    {"name": "U-2 Spy Plane", "src": "https://pollinations.ai/p/U-2%20Spy%20Plane?model=flux", "speed": 500},
    {"name": "Iron Man Suit", "src": "https://pollinations.ai/p/Iron%20Man%20Suit?model=flux", "speed": 1500},
    {"name": "Thunderbird 2", "src": "https://pollinations.ai/p/Thunderbird%202?model=flux", "speed": 540},
    {"name": "Ecto-1 (Ghostbusters)", "src": "https://pollinations.ai/p/Ecto-1%20(Ghostbusters)?model=flux", "speed": 80},
    {"name": "Airwolf Helicopter", "src": "https://pollinations.ai/p/Airwolf%20Helicopter?model=flux", "speed": 300},
    {"name": "Her Majesty's Yacht Britannia", "src": "https://pollinations.ai/p/Her%20Majesty's%20Yacht%20Britannia?model=flux", "speed": 22},
    {"name": "Flying Nimbus", "src": "https://pollinations.ai/p/Flying%20Nimbus?model=flux", "speed": 180},
    {"name": "Thunderbird 4", "src": "https://pollinations.ai/p/Thunderbird%204?model=flux", "speed": 80},
]

# Initialize selected_vehicles as a global variable to be used across different post requests
selected_vehicles = sample(vehicles, 2)

@app.route('/')
def main():
    global selected_vehicles
    selected_vehicles = sample(vehicles, 2)
    return Body(
        Style("""
          body {
              font-family: 'Roboto', sans-serif;
              text-align: center;
              background-color: #f0f8ff;
              margin: 0;
              padding: 0;
              box-sizing: border-box;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              height: 100vh;
              color: #333;
          }
          .vehicle {
              margin: 20px;
              display: inline-block;
              padding: 20px;
              border: 2px solid #ccc;
              border-radius: 10px;
              cursor: pointer;
              transition: transform 0.3s, box-shadow 0.3s;
          }
          .vehicle:hover {
              transform: scale(1.05);
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
          }
          #result {
              margin-top: 20px;
              font-size: 24px;
              color: #ff4500;
              font-weight: bold;
          }
          .next-btn {
              background-color: #ff4500;
              color: white;
              border: none;
              padding: 10px 20px;
              border-radius: 5px;
              cursor: pointer;
              transition: background-color 0.3s;
          }
          .next-btn:hover {
              background-color: #e03e00;
          }
        """),
        H1('Pick the Faster Vehicle'),
        Div(
            *[
                Div(
                    Img(src=vehicle["src"], alt=vehicle["name"], width=100),
                    P(vehicle["name"]),
                    hx_post=f'/select/vehicle?choice={vehicle["name"]}',
                    hx_target='#result',
                    cls='vehicle',
                ) for vehicle in selected_vehicles
            ],
            id='vehicles'
        ),
        Div(id='result')
    )

@app.post('/select/vehicle')
def select_vehicle(choice: str):
    global selected_vehicles
    selected_vehicle = next((v for v in vehicles if v["name"] == choice), None)

    if selected_vehicle:
        faster_vehicle = max(selected_vehicles, key=lambda v: v["speed"])
        if selected_vehicle["name"] == faster_vehicle["name"]:
            result = f"Correct! The {selected_vehicle['name']} is faster."
        else:
            result = f"Try again! The {selected_vehicle['name']} is slower."
    else:
        result = "Incorrect choice!"
    
    return Div(
        P(result, id='result'),
        Button("Next Question", hx_post="/next-question", hx_target="#vehicles", cls='next-btn')
    )

@app.post('/next-question')
def next_question():
    global selected_vehicles
    selected_vehicles = sample(vehicles, 2)
    return Div(
        *[
            Div(
                Img(src=vehicle["src"], alt=vehicle["name"], width=100),
                P(vehicle["name"]),
                hx_post=f"/select/vehicle?choice={vehicle['name']}",
                hx_target='#result',
                cls='vehicle',
            ) for vehicle in selected_vehicles
        ],
        id='vehicles'
    )

serve()