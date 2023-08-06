/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/export.h"

namespace ctre {
namespace phoenixpro {

    /**
     * \brief Get the current timestamp in seconds.
     *
     * \details This will return the current time in seconds, this is
     * the same time that is used in Timestamp.
     *
     * \returns Current time in seconds.
     */
    CTREXPORT double GetCurrentTimeSeconds();
    /**
     * \brief Get whether the program is running in simulation.
     *
     * \returns `true` if in simulation
     */
    CTREXPORT bool IsSimulation();

}
}
