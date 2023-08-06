/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/StatusCodes.h"
#include "ctre/phoenix/export.h"
#include "ctre/phoenix/platform/canframe.hpp"
#include <set>
#include <sstream>
#include <stdint.h>

namespace ctre
{
    namespace phoenix
    {
        namespace platform
        {
            namespace can
            {

                CTREXPORT StatusCode Network_GetLastTx(std::string const &canbus, uint32_t arbId, canframe_t &frame);
                CTREXPORT bool Network_ChangeTxPeriod(std::string const &canbus, uint32_t arbId, int32_t periodMs);

                CTREXPORT StatusCode Network_SendTxFrame(std::string const &canbus, canframe_t const &frame);
                CTREXPORT StatusCode Network_SendPeriodicTxFrame(std::string const &canbus, canframe_t const &frame, int32_t periodMs);
                CTREXPORT StatusCode Network_UpdatePeriodicTxFrame(std::string const &canbus, canframe_t const &frame);
                CTREXPORT StatusCode Network_StopPeriodicTxFrame(std::string const &canbus, uint32_t arbId);

                CTREXPORT StatusCode Network_GetRxFrame(char const *canbus, uint32_t arbId, canframe_t &frame, uint32_t timeoutMs);
                CTREXPORT StatusCode Network_WaitForRxFrames(char const *canbus, std::set<uint32_t> const &arbIds, uint16_t timeoutMs);

            } // namespace can
        } // namespace platform
    } // namespace phoenix
} // namespace ctre