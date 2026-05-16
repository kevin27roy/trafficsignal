let autoInterval = null

// -----------------------------------
// Fetch Current State
// -----------------------------------

async function updateState() {

    try {

        const response =
            await fetch('/state')

        const data =
            await response.json()

        updateUI(data)

    } catch (error) {

        console.error(
            "State update failed:",
            error
        )
    }
}

// -----------------------------------
// Manual Signal Control
// -----------------------------------

async function manualAction(action) {

    // Stop RL auto mode
    stopAuto()

    try {

        const response =
            await fetch('/step', {

            method: 'POST',

            headers: {
                'Content-Type':
                    'application/json'
            },

            body: JSON.stringify({
                action: action
            })
        })

        const data =
            await response.json()

        updateUI(data)

    } catch (error) {

        console.error(
            "Manual action failed:",
            error
        )
    }
}

// -----------------------------------
// Single RL Step
// -----------------------------------

async function autoStep() {

    try {

        const response =
            await fetch('/auto')

        const data =
            await response.json()

        updateUI(data)

    } catch (error) {

        console.error(
            "RL auto step failed:",
            error
        )
    }
}

// -----------------------------------
// Start Continuous RL Simulation
// -----------------------------------

function autoRun() {

    // Prevent duplicate loops
    if (autoInterval !== null)
        return

    autoInterval = setInterval(() => {

        autoStep()

    }, 500)
}

// -----------------------------------
// Stop RL Simulation
// -----------------------------------

function stopAuto() {

    if (autoInterval !== null) {

        clearInterval(autoInterval)

        autoInterval = null
    }
}

// -----------------------------------
// Reset Environment
// -----------------------------------

async function resetEnv() {

    stopAuto()

    try {

        const response =
            await fetch('/reset', {

            method: 'POST'
        })

        const data =
            await response.json()

        updateUI(data)

    } catch (error) {

        console.error(
            "Reset failed:",
            error
        )
    }
}

// -----------------------------------
// Update Frontend UI
// -----------------------------------

function updateUI(data) {

    // Render cars
    renderCars(
        "north-cars",
        data.queues[0]
    )

    renderCars(
        "south-cars",
        data.queues[1]
    )

    renderCars(
        "east-cars",
        data.queues[2]
    )

    renderCars(
        "west-cars",
        data.queues[3]
    )

    // Total vehicles
    const total =
        data.queues[0] +
        data.queues[1] +
        data.queues[2] +
        data.queues[3]

    document.getElementById(
        "total"
    ).innerText = total

    // Reward
    if (data.reward !== undefined) {

        document.getElementById(
            "reward"
        ).innerText =
            Number(data.reward).toFixed(2)
    }

    // Phase label
    const phaseLabel =
        document.getElementById(
            "phase-label"
        )

    if (data.phase === 0) {

        phaseLabel.innerText =
            "North-South"

    } else {

        phaseLabel.innerText =
            "East-West"
    }

    // Traffic lights
    updateTrafficLights(
        data.phase
    )
}

// -----------------------------------
// Render Cars
// -----------------------------------

function renderCars(containerId, count) {

    const container =
        document.getElementById(
            containerId
        )

    container.innerHTML = ""

    for (let i = 0; i < count; i++) {

        const car =
            document.createElement(
                "div"
            )

        car.classList.add("car")

        container.appendChild(car)
    }
}

// -----------------------------------
// Traffic Light Animation
// -----------------------------------

function updateTrafficLights(phase) {

    const red =
        document.getElementById(
            "red-light"
        )

    const green =
        document.getElementById(
            "green-light"
        )

    if (phase === 0) {

        green.style.opacity = "1"

        red.style.opacity = "0.3"

    } else {

        green.style.opacity = "0.3"

        red.style.opacity = "1"
    }
}

// -----------------------------------
// Initial Load
// -----------------------------------

updateState()