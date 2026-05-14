async function updateState() {

    try {

        const response = await fetch('/state')

        const data = await response.json()

        updateUI(data)

    } catch (error) {

        console.error("Failed to fetch state:", error)
    }
}

async function manualAction(action) {

    try {

        const response = await fetch('/step', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                action: action
            })
        })

        const data = await response.json()

        updateUI(data)

    } catch (error) {

        console.error("Manual action failed:", error)
    }
}

async function autoRun() {

    try {

        const response = await fetch('/auto')

        const data = await response.json()

        updateUI(data)

    } catch (error) {

        console.error("RL auto step failed:", error)
    }
}

async function resetEnv() {

    try {

        const response = await fetch('/reset', {

            method: 'POST'
        })

        const data = await response.json()

        updateUI(data)

    } catch (error) {

        console.error("Reset failed:", error)
    }
}

function updateUI(data) {

    // Render animated cars
    renderCars("north-cars", data.queues[0])
    renderCars("south-cars", data.queues[1])
    renderCars("east-cars", data.queues[2])
    renderCars("west-cars", data.queues[3])

    // Total vehicle count
    const total =
        data.queues[0] +
        data.queues[1] +
        data.queues[2] +
        data.queues[3]

    document.getElementById("total").innerText =
        total

    // Reward
    if (data.reward !== undefined) {

        document.getElementById("reward").innerText =
            Number(data.reward).toFixed(2)
    }

    // Phase label
    const phaseLabel =
        document.getElementById("phase-label")

    if (data.phase === 0) {

        phaseLabel.innerText =
            "North-South"

    } else {

        phaseLabel.innerText =
            "East-West"
    }

    // Traffic light colors
    updateTrafficLights(data.phase)
}

function renderCars(containerId, count) {

    const container =
        document.getElementById(containerId)

    container.innerHTML = ""

    for (let i = 0; i < count; i++) {

        const car =
            document.createElement("div")

        car.classList.add("car")

        container.appendChild(car)
    }
}

function updateTrafficLights(phase) {

    const red =
        document.getElementById("red-light")

    const green =
        document.getElementById("green-light")

    if (phase === 0) {

        green.style.opacity = "1"
        red.style.opacity = "0.3"

    } else {

        green.style.opacity = "0.3"
        red.style.opacity = "1"
    }
}

// Initial load
updateState()

// Auto refresh every 2 seconds
setInterval(updateState, 2000)