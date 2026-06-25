// -----------------------------
// Loading Screen
// -----------------------------
window.addEventListener("load", () => {

    const loader = document.getElementById("loading-screen");
    const app = document.getElementById("app");

    // Wait for intro animation
    setTimeout(() => {

        loader.style.opacity = "0";
        loader.style.transition = "0.8s";

        setTimeout(() => {

            loader.style.display = "none";

            app.style.display = "block";

            app.animate([
                {
                    opacity:0,
                    transform:"translateY(20px)"
                },
                {
                    opacity:1,
                    transform:"translateY(0px)"
                }

            ],{

                duration:700,
                easing:"ease-out"

            });

        },800);

    },4200);

});

// -----------------------------
// Live Clock
// -----------------------------
function updateClock(){

    const now = new Date();

    const h = String(now.getHours()).padStart(2,'0');
    const m = String(now.getMinutes()).padStart(2,'0');
    const s = String(now.getSeconds()).padStart(2,'0');

    document.getElementById("clock").innerHTML =
        `${h}:${m}:${s}`;

}

setInterval(updateClock,1000);

updateClock();

// -----------------------------
// Fake Dashboard Numbers
// (Until Flask API is added)
// -----------------------------

function random(min,max){

    return Math.floor(
        Math.random()*(max-min+1)
    )+min;

}

function updateDashboard(){

    const fps = random(28,60);

    const faces = random(0,3);

    document.getElementById("fps").innerHTML = fps;

    document.getElementById("faces").innerHTML = faces;

}

setInterval(updateDashboard,1000);

updateDashboard();

// -----------------------------
// Smooth Glow Effect
// -----------------------------
document.addEventListener("mousemove",(e)=>{

    const glow1=document.querySelector(".glow1");
    const glow2=document.querySelector(".glow2");

    const x=e.clientX/window.innerWidth;
    const y=e.clientY/window.innerHeight;

    glow1.style.transform=
    `translate(${x*35}px,${y*35}px)`;

    glow2.style.transform=
    `translate(${-x*35}px,${-y*35}px)`;

});

// -----------------------------
// Glass Hover Animation
// -----------------------------
const cards=document.querySelectorAll(".glass");

cards.forEach(card=>{

    card.addEventListener("mouseenter",()=>{

        card.style.transform="translateY(-6px)";

    });

    card.addEventListener("mouseleave",()=>{

        card.style.transform="translateY(0px)";

    });

});

// -----------------------------
// Camera Fade In
// -----------------------------
window.addEventListener("load",()=>{

    const cam=document.querySelector(".camera-frame");

    setTimeout(()=>{

        cam.animate([

            {
                opacity:0,
                transform:"scale(.97)"
            },

            {
                opacity:1,
                transform:"scale(1)"
            }

        ],{

            duration:900,
            easing:"ease-out"

        });

    },4400);

});

// -----------------------------
// Live Dot Pulse
// -----------------------------
setInterval(()=>{

    const dot=document.querySelector(".live-dot");

    dot.animate([

        {

            transform:"scale(1)"

        },

        {

            transform:"scale(1.8)"

        },

        {

            transform:"scale(1)"

        }

    ],{

        duration:1000

    });

},1000);

// -----------------------------
// Scan Glow Flicker
// -----------------------------
setInterval(()=>{

    const scan=document.querySelector(".scan-line");

    scan.style.opacity="0.5";

    setTimeout(()=>{

        scan.style.opacity="1";

    },120);

},3000);

// -----------------------------
// Footer Year
// -----------------------------
const footer=document.querySelector("footer");

footer.innerHTML=footer.innerHTML.replace(
"2026",
new Date().getFullYear()
);

// ==========================================
// END
// ==========================================