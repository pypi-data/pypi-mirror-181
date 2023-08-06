/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/export.h"
#include <stdint.h>

namespace ctre
{
    namespace phoenix
    {
        namespace platform
        {

            CTREXPORT void ReportError(int isError, int32_t errorCode, int isLVCode, const char *details,
                                       const char *location, const char *callStack);

        } // namespace platform
    } // namespace phoenix
} // namespace ctre
