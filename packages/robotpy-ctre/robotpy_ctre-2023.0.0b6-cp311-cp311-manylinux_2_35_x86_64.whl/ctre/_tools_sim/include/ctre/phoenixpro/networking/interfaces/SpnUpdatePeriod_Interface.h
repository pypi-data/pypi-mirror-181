/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/export.h"
#include "ctre/phoenixpro/networking/interfaces/DeviceEncoding_Interface.h"
#include "stdint.h"

#ifdef __cplusplus
extern "C"
{
#endif
    CTREXPORT int c_ctre_phoenixpro_SetUpdateFrequency(Context context, const char *network, uint32_t deviceHash, uint16_t spn, double frequencyHz, double timeoutSeconds);
#ifdef __cplusplus
}
#endif
