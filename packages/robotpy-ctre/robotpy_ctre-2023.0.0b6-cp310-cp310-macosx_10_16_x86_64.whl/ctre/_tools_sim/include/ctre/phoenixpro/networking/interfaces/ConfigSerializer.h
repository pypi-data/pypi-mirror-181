/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/export.h"
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif
    /* Note: This returns a malloc'd char array that caller needs to free */
    CTREXPORT int c_ctre_phoenixpro_serialize_double(int spn, double value, char **str);
    /* Note: This returns a malloc'd char array that caller needs to free */
    CTREXPORT int c_ctre_phoenixpro_serialize_int(int spn, int value, char **str);
    /* Note: This returns a malloc'd char array that caller needs to free */
    CTREXPORT int c_ctre_phoenixpro_serialize_bool(int spn, bool value, char **str);
    CTREXPORT int c_ctre_phoenixpro_serialize_pgn(int spn, uint16_t frame_index, uint16_t framePeriodMs, char **str);
    CTREXPORT int c_ctre_phoenixpro_deserialize_double(int spn, const char *str, size_t strlen, double *val);
    CTREXPORT int c_ctre_phoenixpro_deserialize_int(int spn, const char *str, size_t strlen, int *val);
    CTREXPORT int c_ctre_phoenixpro_deserialize_bool(int spn, const char *str, size_t strlen, bool *val);
    CTREXPORT int c_ctre_phoenixpro_deserialize_pgn(int spn, const char *str, size_t strlen, uint16_t *frame_index, uint16_t *framePeriodMs);
#ifdef __cplusplus
}
#endif