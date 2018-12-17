/*
 * Copyright (c) 2018 Anthony Beaucamp.
 *
 * This software is provided 'as-is', without any express or implied warranty.
 * In no event will the authors be held liable for any damages arising from
 * the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 *   1. The origin of this software must not be misrepresented * you must not
 *   claim that you wrote the original software. If you use this software in a
 *   product, an acknowledgment in the product documentation would be
 *   appreciated but is not required.
 *
 *   2. Altered source versions must be plainly marked as such, and must not
 *   be misrepresented as being the original software.
 *
 *   3. This notice may not be removed or altered from any distribution.
 *
 *   4. The names of this software and/or it's copyright holders may not be
 *   used to endorse or promote products derived from this software without
 *   specific prior written permission.
 *
 * Adapted from: Bill Buckels
 */
 
//	Helper functions for Apple II Double Hi-Res Mode
//	Last modified: 2018/01/25

// Bitmasks for color assignement
unsigned char DHRBytes[16][4] = {
	{0x00,0x00,0x00,0x00},
	{0x08,0x11,0x22,0x44},
	{0x11,0x22,0x44,0x08},
	{0x19,0x33,0x66,0x4C},
	{0x22,0x44,0x08,0x11},
	{0x2A,0x55,0x2A,0x55},
	{0x33,0x66,0x4C,0x19},
	{0x3B,0x77,0x6E,0x5D},
	{0x44,0x08,0x11,0x22},
	{0x4C,0x19,0x33,0x66},
	{0x55,0x2A,0x55,0x2A},
	{0x5D,0x3B,0x77,0x6E},
	{0x66,0x4C,0x19,0x33},
	{0x6E,0x5D,0x3B,0x77},
	{0x77,0x6E,0x5D,0x3B},
	{0x7F,0x7F,0x7F,0x7F}};	

// DHR base array: provides base address for 192 hires scanlines
unsigned int DHRBases[192] = {
	0x2000, 0x2400, 0x2800, 0x2C00, 0x3000, 0x3400, 0x3800, 0x3C00,
	0x2080, 0x2480, 0x2880, 0x2C80, 0x3080, 0x3480, 0x3880, 0x3C80,
	0x2100, 0x2500, 0x2900, 0x2D00, 0x3100, 0x3500, 0x3900, 0x3D00,
	0x2180, 0x2580, 0x2980, 0x2D80, 0x3180, 0x3580, 0x3980, 0x3D80,
	0x2200, 0x2600, 0x2A00, 0x2E00, 0x3200, 0x3600, 0x3A00, 0x3E00,
	0x2280, 0x2680, 0x2A80, 0x2E80, 0x3280, 0x3680, 0x3A80, 0x3E80,
	0x2300, 0x2700, 0x2B00, 0x2F00, 0x3300, 0x3700, 0x3B00, 0x3F00,
	0x2380, 0x2780, 0x2B80, 0x2F80, 0x3380, 0x3780, 0x3B80, 0x3F80,
	0x2028, 0x2428, 0x2828, 0x2C28, 0x3028, 0x3428, 0x3828, 0x3C28,
	0x20A8, 0x24A8, 0x28A8, 0x2CA8, 0x30A8, 0x34A8, 0x38A8, 0x3CA8,
	0x2128, 0x2528, 0x2928, 0x2D28, 0x3128, 0x3528, 0x3928, 0x3D28,
	0x21A8, 0x25A8, 0x29A8, 0x2DA8, 0x31A8, 0x35A8, 0x39A8, 0x3DA8,
	0x2228, 0x2628, 0x2A28, 0x2E28, 0x3228, 0x3628, 0x3A28, 0x3E28,
	0x22A8, 0x26A8, 0x2AA8, 0x2EA8, 0x32A8, 0x36A8, 0x3AA8, 0x3EA8,
	0x2328, 0x2728, 0x2B28, 0x2F28, 0x3328, 0x3728, 0x3B28, 0x3F28,
	0x23A8, 0x27A8, 0x2BA8, 0x2FA8, 0x33A8, 0x37A8, 0x3BA8, 0x3FA8,
	0x2050, 0x2450, 0x2850, 0x2C50, 0x3050, 0x3450, 0x3850, 0x3C50,
	0x20D0, 0x24D0, 0x28D0, 0x2CD0, 0x30D0, 0x34D0, 0x38D0, 0x3CD0,
	0x2150, 0x2550, 0x2950, 0x2D50, 0x3150, 0x3550, 0x3950, 0x3D50,
	0x21D0, 0x25D0, 0x29D0, 0x2DD0, 0x31D0, 0x35D0, 0x39D0, 0x3DD0,
	0x2250, 0x2650, 0x2A50, 0x2E50, 0x3250, 0x3650, 0x3A50, 0x3E50,
	0x22D0, 0x26D0, 0x2AD0, 0x2ED0, 0x32D0, 0x36D0, 0x3AD0, 0x3ED0,
	0x2350, 0x2750, 0x2B50, 0x2F50, 0x3350, 0x3750, 0x3B50, 0x3F50,
	0x23D0, 0x27D0, 0x2BD0, 0x2FD0, 0x33D0, 0x37D0, 0x3BD0, 0x3FD0};

// Addresses for AUX bank copying
unsigned char *dhrmain = (unsigned char*)0xC054;
unsigned char *dhraux = (unsigned char*)0xC055;	
unsigned char *dhrptr, dhrpixel;

void SetDHRPointer(unsigned int x, unsigned int y)
{
	// Compute 7 pixels block address
	unsigned int xoff;
	dhrpixel = (x%7);
	xoff = (x/7)*2;
	if (dhrpixel > 3) { ++xoff; }
	dhrptr = (unsigned char *) (DHRBases[y] + xoff);
}

void SetDHRColor(unsigned char color)
{
	// Use bitmasks to assign the relevant pixel
	switch(dhrpixel) {
		case 0: *dhraux = 0; // select auxilliary memory 
				*dhrptr &= 0x70;
				*dhrptr |= (DHRBytes[color][0] & 0x0f);
				*dhrmain = 0; // reset to main memory 
				break;
		case 1: *dhraux = 0; // select auxilliary memory 
				*dhrptr &= 0x0f;
				*dhrptr |= (DHRBytes[color][0] & 0x70);
				*dhrmain = 0; // reset to main memory 
				*dhrptr &= 0x7e;
				*dhrptr |= (DHRBytes[color][1] & 0x01);
				break;
		case 2: *dhrptr &= 0x61;
				*dhrptr |= (DHRBytes[color][1] & 0x1e);
				break;
		case 3: *dhrptr &= 0x1f;
				*dhrptr |= (DHRBytes[color][1] & 0x60);
				*dhraux = 0; // select auxilliary memory 
				*dhrptr++;   // advance offset in frame 
				*dhrptr &= 0x7c;
				*dhrptr |= (DHRBytes[color][2] & 0x03);
				*dhrmain = 0; // reset to main memory 
				break;
		case 4: *dhraux = 0; // select auxilliary memory 
				*dhrptr &= 0x43;
				*dhrptr |= (DHRBytes[color][2] & 0x3c);
				*dhrmain = 0; // reset to main memory 
				break;
		case 5: *dhraux = 0; // select auxilliary memory 
				*dhrptr &= 0x3f;
				*dhrptr |= (DHRBytes[color][2] & 0x40);
				*dhrmain = 0; // reset to main memory 
				*dhrptr &= 0x78;
				*dhrptr |= (DHRBytes[color][3] & 0x07);
				break;
		case 6: *dhrptr &= 0x07;
				*dhrptr |= (DHRBytes[color][3] & 0x78);
				break;
	}
}

unsigned char GetDHRColor()
{
	unsigned char val1, val2, off1, off2, msk1, msk2, color;

	// Use bitmsks to retrieve the relevant pixel
	switch(dhrpixel) {
		case 0: *dhraux = 0; // select auxilliary memory 
				val1 = *dhrptr;
				off1 = 0;
				msk1 = 0x0f;
				msk2 = 0;
				*dhrmain = 0; // reset to main memory 
				break;
		case 1: *dhraux = 0; // select auxilliary memory 
				val1 = *dhrptr;
				off1 = 0;
				msk1 = 0x70;
				*dhrmain = 0; // reset to main memory 
				val2 = *dhrptr;
				off2 = 1;
				msk2 = 0x01;
				break;
		case 2: val1 = *dhrptr;
				off1 = 1;
				msk1 = 0x1e;
				msk2 = 0;
				break;
		case 3: val1 = *dhrptr;
				off1 = 1;
				msk1 = 0x60;
				*dhrptr++;      // advance off in frame 
				val2 = *dhrptr;
				off2 = 2;
				msk2 = 0x03;
				break;
		case 4: *dhraux = 0; // select auxilliary memory 
				val1 = *dhrptr;
				off1 = 2;
				msk1 = 0x3c;
				msk2 = 0;
				*dhrmain = 0; // reset to main memory 
				break;
		case 5: *dhraux = 0; // select auxilliary memory 
				val1 = *dhrptr;
				off1 = 2;
				msk1 = 0x40;
				*dhrmain = 0; // reset to main memory 
				val2 = *dhrptr;
				off2 = 3;
				msk2 = 0x07;
				break;
		case 6: val1 = *dhrptr;
				off1 = 3;
				msk1 = 0x78;
				msk2 = 0;
				break;
	}

	// Compare masked values with DHR color list
	for (color=0; color<16; color++) {
		if (!msk2) {
			if ((val1 & msk1) == (DHRBytes[color][off1] & msk1)) { return color; }
		} else {
			if ((val1 & msk1) == (DHRBytes[color][off1] & msk1) && 
				(val2 & msk2) == (DHRBytes[color][off2] & msk2)) { return color; }
		}
	}
	return 0;
}
