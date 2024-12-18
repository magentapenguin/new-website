import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { SAOPass } from 'three/addons/postprocessing/SAOPass.js';
import { TAARenderPass } from 'three/addons/postprocessing/TAARenderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

import WebGL from 'three/addons/capabilities/WebGL.js';

const container = document.getElementById('model');



const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0xffffff, 1);
renderer.setSize(container.clientWidth, container.clientHeight);
const controls = new OrbitControls(camera, renderer.domElement);

const composer = new EffectComposer( renderer );
const firstPass = new SAOPass( scene, camera );
firstPass.params.saoBias = 0.5;
firstPass.params.saoIntensity = 0.15;
firstPass.params.saoScale = 100;
firstPass.params.saoKernelRadius = 100;
firstPass.params.saoMinResolution = 0;
const renderPass = new TAARenderPass( scene, camera );
const outputPass = new OutputPass();

composer.addPass( renderPass );
composer.addPass( firstPass );
composer.addPass( outputPass );

const light = new THREE.AmbientLight(0xffffff, 10);
scene.add(light);
const pointlight1 = new THREE.PointLight(0xffffff, 20);
pointlight1.position.set(3, 4, 0);
scene.add(pointlight1);
const light2 = new THREE.RectAreaLight(0xffffff, 30);
light2.position.set(0, 4, 7);
scene.add(light2);
// floor plane
const geometry = new THREE.PlaneGeometry(10, 10, 10, 10);
const material = new THREE.MeshLambertMaterial({ color: 0x888888, side: THREE.DoubleSide});
const plane = new THREE.Mesh(geometry, material);
plane.rotation.x = Math.PI / 2;
scene.add(plane);

const loader = new GLTFLoader();
container.appendChild(renderer.domElement);

camera.position.set(0.2, 3, 2);
camera.lookAt(0, 0, 0);
controls.update();

let model;

loader.load(container.dataset.file, function (gltf) {
    scene.add(gltf.scene);
    model = gltf.scene;
    model.position.set(0, 0, 0);
    model.scale.set(0.1, 0.1, 0.1);
}, undefined, function (error) {
    console.error(error);
});

function renderScene() {
    requestAnimationFrame(renderScene);
    controls.update();
    //renderer.render(scene, camera);
    composer.render();
}
if (!WebGL.isWebGL2Available()) {
    container.appendChild(WebGL.getWebGL2ErrorMessage());
} else {
    renderScene();
}

function resize() {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
    composer.setSize(container.clientWidth, container.clientHeight);
    
}

window.addEventListener('resize', resize);


function fullscreen() {
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        container.requestFullscreen();
    }
    resize();
}

document.getElementById('fullscreen').addEventListener('click', fullscreen);
