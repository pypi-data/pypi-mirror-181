/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/export.h"
#include <cstdint>

#ifdef __cplusplus
extern "C"
{
#endif

    CTREXPORT void c_ctre_phoenix_report_error(int isError, int32_t errorCode, int isLVCode, const char *details,
                                               const char *location, const char *callStack);

#ifdef __cplusplus
}
#endif
