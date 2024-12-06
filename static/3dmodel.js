import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
/*
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { SMAAPass } from 'three/addons/postprocessing/SMAAPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
*/
import WebGL from 'three/addons/capabilities/WebGL.js';

const container = document.getElementById('model');



const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer( { antialias: true } );
const controls = new OrbitControls(camera, renderer.domElement);
/*
const composer = new EffectComposer( renderer );
const firstPass = new SMAAPass( container.clientWidth * renderer.getPixelRatio(), container.clientHeight * renderer.getPixelRatio() );
const renderPass = new RenderPass( scene, camera );
const outputPass = new OutputPass();
composer.addPass( renderPass );
composer.addPass( firstPass );
composer.addPass( outputPass );
*/
const light = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(light);
const pointlight = new THREE.SpotLight(0xffffff, 30 ,0, Math.PI / 2);
scene.add(pointlight);
const loader = new GLTFLoader();
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x222222, 1);
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

camera.position.set(0,10,0);

let model;

loader.load('static/teapot.glb', function (gltf) {
    scene.add(gltf.scene);
    model = gltf.scene;
    pointlight.target = model;
    console.log(gltf);
}, undefined, function (error) {
    console.error(error);
});

function renderScene() {
    requestAnimationFrame(renderScene);
    controls.update();
    pointlight.position.set(camera.position.x, camera.position.y, camera.position.z);
    pointlight.position.normalize().multiplyScalar(20);
    renderer.render(scene, camera);
    //composer.render();
}
if (!WebGL.isWebGL2Available()) {
    container.appendChild(THREE.WEBGL.getWebGL2ErrorMessage());
} else {
    renderScene();
}

function resize() {
    camera.aspect = container.innerWidth / container.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.innerWidth, container.innerHeight);
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
