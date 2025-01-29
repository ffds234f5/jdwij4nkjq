document.addEventListener("DOMContentLoaded", function () {
    let cat = document.getElementById("cat");

    let screenWidth = window.innerWidth;
    let screenHeight = window.innerHeight;
    let speed = 3;
    let direction = 1;
    let isDragging = false;
    let moveInterval;
    let shiftX = 0, shiftY = 0;

    function updateScreenSize() {
        screenWidth = window.innerWidth;
        screenHeight = window.innerHeight;
    }

    function updateCatGif() {
        if (isDragging) {
            cat.src = "/static/images/cat_drag.gif";
        } else if (direction === 1) {
            cat.src = "/static/images/cat_run_right.gif";
        } else {
            cat.src = "/static/images/cat_run_left.gif";
        }
    }

    function moveCat() {
        if (isDragging) return;

        let newX = cat.offsetLeft + speed * direction;


        if (newX <= 0) {
            newX = 0;
            direction = 1;
        } else if (newX >= screenWidth - cat.clientWidth) {
            newX = screenWidth - cat.clientWidth;
            direction = -1;
        }

        cat.style.left = newX + "px";
    }

    function randomStartPosition() {
        return {
            x: Math.random() * (screenWidth - 100),
            y: Math.random() * (screenHeight - 100)
        };
    }

    updateScreenSize();
    let startPos = randomStartPosition();
    cat.style.position = "fixed";
    cat.style.left = startPos.x + "px";
    cat.style.top = `${screenHeight - cat.clientHeight - 20}px`;
    cat.style.zIndex = "999999";

    moveInterval = setInterval(moveCat, 20);
    updateCatGif();

    cat.addEventListener("mousedown", function (event) {
        isDragging = true;
        clearInterval(moveInterval);
        updateCatGif();

        let rect = cat.getBoundingClientRect();
        shiftX = event.clientX - rect.left;
        shiftY = event.clientY - rect.top;

        function onMouseMove(event) {
            let newX = event.clientX - shiftX;
            let newY = event.clientY - shiftY;

            newX = Math.max(0, Math.min(screenWidth - cat.clientWidth, newX));
            newY = Math.max(screenHeight - cat.clientHeight - 20, newY);

            cat.style.left = newX + "px";
            cat.style.top = newY + "px";
        }

        document.addEventListener("mousemove", onMouseMove);

        document.addEventListener("mouseup", function () {
            document.removeEventListener("mousemove", onMouseMove);
            isDragging = false;
            direction = Math.random() < 0.5 ? -1 : 1;
            moveInterval = setInterval(moveCat, 20);
            updateCatGif();
        }, { once: true });
    });

    setInterval(() => {
        if (!isDragging && Math.random() < 0.05) {
            direction *= -1;
            updateCatGif();
        }
    }, 2000);

    setInterval(() => {
        if (!isDragging && Math.random() < 0.1) {
            clearInterval(moveInterval);
            cat.src = "/static/images/cat_idle.gif";
            setTimeout(() => {
                moveInterval = setInterval(moveCat, 20);
                updateCatGif();
            }, 2000);
        }
    }, 5000);

    window.addEventListener("resize", updateScreenSize);
});
