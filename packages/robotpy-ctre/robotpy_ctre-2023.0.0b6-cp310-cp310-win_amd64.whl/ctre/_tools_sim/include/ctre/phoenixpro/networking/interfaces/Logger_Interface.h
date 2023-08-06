/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/StatusCodes.h"
#include "ctre/phoenix/export.h"
#include <string>

#ifdef __cplusplus
extern "C"
{
#endif
    CTREXPORT int c_Logger_Log(ctre::phoenix::StatusCode code, const char *device, const char *func, int hierarchy, const char *stacktrace);
#ifdef __cplusplus
}
#endif
