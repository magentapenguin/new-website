import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const container = document.getElementById('model');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
const composer = new EffectComposer( renderer );
const ssaoPass = new SSAOPass( scene, camera, window.innerWidth, window.innerHeight );
const renderPass = new RenderPass( scene, camera );
const outputPass = new OutputPass();
composer.addPass( renderPass );
composer.addPass( ssaoPass );
composer.addPass( outputPass );

const light = new THREE.AmbientLight(0xffffff, 0.2);
scene.add(light);
const pointlight = new THREE.SpotLight(0xffffff, 20,0, Math.PI / 2);
pointlight.position.set(0, 0, 20);
pointlight.rotation.x = Math.PI / 2;
scene.add(pointlight);
const loader = new GLTFLoader();

renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

camera.position.set(0,10,0);

let model;

loader.load('static/teapot.glb', function (gltf) {
    scene.add(gltf.scene);
    model = gltf.scene;
}, undefined, function (error) {
    console.error(error);
});

function animate() {
    requestAnimationFrame(animate);
    const timer = performance.now();
    try {
        model.rotation.x = timer * 0.0002;
        model.rotation.y = timer * 0.0001;
    } catch (e) {}
    //renderer.render(scene, camera);
    composer.render();
}

animate();

window.addEventListener('resize', function () {
    camera.aspect = container.innerWidth / container.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.innerWidth, container.innerHeight);
});

