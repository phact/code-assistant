from fasthtml.common import *

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return Html(
        Head(
            Title('Minecraft Clone'),
            Script(src='https://cdn.babylonjs.com/babylon.js'),
            Script(src='https://code.jquery.com/pep/0.4.3/pep.js'),
            Script(src='https://unpkg.com/htmx.org@1.6.1'),
            Script(src='https://unpkg.com/htmx.org/dist/ext/json-enc.js'),
            Style('''
                body, html { margin: 0; overflow: hidden; height: 100%; }
                canvas { display: block; width: 100%; height: 100%; }
            ''')
        ),
        Body(
            Canvas(id='renderCanvas', touch_action='none'),
            Script('''
                const canvas = document.getElementById("renderCanvas");
                const engine = new BABYLON.Engine(canvas, true);
                
                const createScene = function () {
                    const scene = new BABYLON.Scene(engine);
                    
                    const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 1.6, -10), scene);
                    camera.setTarget(BABYLON.Vector3.Zero());
                    camera.attachControl(canvas, true);
                    
                    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
                    
                    const groundMaterial = new BABYLON.StandardMaterial("groundMat", scene);
                    groundMaterial.diffuseColor = new BABYLON.Color3(0.4, 0.3, 0.3);

                    const treeTrunkMaterial = new BABYLON.StandardMaterial("trunkMat", scene);
                    treeTrunkMaterial.diffuseColor = new BABYLON.Color3(0.55, 0.27, 0.07);

                    const leavesMaterial = new BABYLON.StandardMaterial("leavesMat", scene);
                    leavesMaterial.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);

                    const dirtMaterial = new BABYLON.StandardMaterial("dirtMat", scene);
                    dirtMaterial.diffuseColor = new BABYLON.Color3(0.6, 0.4, 0.2);

                    // Create large ground
                    const ground = BABYLON.MeshBuilder.CreateGround("ground", {width: 100, height: 100}, scene);
                    ground.position.y = -0.5;
                    ground.material = groundMaterial;

                    const createBlock = function(x, y, z, material) {
                        const block = BABYLON.MeshBuilder.CreateBox("block", { size: 1 }, scene);
                        block.position = new BABYLON.Vector3(x, y, z);
                        block.material = material;
                        return block;
                    };

                    const blocks = [];
                    // Add tree trunk
                    for (let y = 0; y < 4; y++) {
                        blocks.push(createBlock(0, y, 0, treeTrunkMaterial));
                    }
                    // Add leaves
                    for (let y = 4; y < 6; y++) {
                        for (let x = -1; x <= 1; x++) {
                            for (let z = -1; z <= 1; z++) {
                                blocks.push(createBlock(x, y, z, leavesMaterial));
                            }
                        }
                    }
                    // Add layer of brown cubes (dirt) at ground level
                    for (let x = -50; x <= 50; x++) {
                        for (let z = -50; z <= 50; z++) {
                            blocks.push(createBlock(x, 0, z, dirtMaterial));
                        }
                    }

                    canvas.addEventListener('pointerdown', function(evt) {
                        const pickResult = scene.pick(evt.clientX, evt.clientY);
                        if (pickResult.hit) {
                            if (evt.button === 0) { // Left Click
                                const normal = pickResult.getNormal(true);
                                const selectedBlock = pickResult.pickedMesh;
                                const newBlock = createBlock(selectedBlock.position.x + normal.x, selectedBlock.position.y + normal.y, selectedBlock.position.z + normal.z, leavesMaterial);
                                blocks.push(newBlock);
                            } else if (evt.button === 2) { // Right Click
                                const selectedBlock = pickResult.pickedMesh;
                                const index = blocks.indexOf(selectedBlock);
                                if (index > -1) {
                                    selectedBlock.dispose();
                                    blocks.splice(index, 1);
                                }
                            }
                        }
                    });
                    
                    // Handle double clicks to change block color
                    canvas.addEventListener('dblclick', function(evt) {
                        const pickResult = scene.pick(evt.clientX, evt.clientY);
                        if (pickResult.hit) {
                            const selectedBlock = pickResult.pickedMesh;
                            const newColorIndex = Math.floor(Math.random() * 10);
                            selectedBlock.material = materials[newColorIndex];
                        }
                    });

                    return scene;
                };

                const scene = createScene();
                engine.runRenderLoop(function () {
                    scene.render();
                });

                window.addEventListener('resize', function () {
                    engine.resize();
                });
            ''', type='module')
        )
    )

serve()