// Conexión compartida a Firebase (Auth + Firestore) para todas las páginas.
// La apiKey de Firebase es pública por diseño; la seguridad la dan las reglas de Firestore (firestore.rules).
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

export const firebaseConfig = {
  apiKey: "AIzaSyDyA-Arc8B-t0qX4VPFx7N3OXRoHiLyzNw",
  authDomain: "kronosmedicine.firebaseapp.com",
  projectId: "kronosmedicine",
  storageBucket: "kronosmedicine.firebasestorage.app",
  messagingSenderId: "175147519932",
  appId: "1:175147519932:web:1bad92b6179f5b7c51a5b9",
  measurementId: "G-WK2VR4EE8B"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);

// Páginas privadas: si no hay sesión, manda a login.html y regresa aquí después.
export function requireUser(callback) {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      document.getElementById('app-body')?.classList.remove('hidden');
      callback(user);
    } else {
      const next = encodeURIComponent(location.pathname.split('/').pop() + location.search + location.hash);
      location.href = `login.html?next=${next}`;
    }
  });
}

export function salir() {
  signOut(auth).then(() => { location.href = 'index.html'; });
}
