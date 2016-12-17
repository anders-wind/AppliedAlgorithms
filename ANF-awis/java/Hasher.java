
import java.util.*;

public class Hasher
{
    
	private static final int[] linear = {0x21ae4036,0x32435171,0xac3338cf,0xea97b40c,0x0e504b22,0x9ff9a4ef,0x111d014d,0x934f3787,0x6cd079bf,0x69db5c31,0xdf3c28ed,0x40daf2ad,0x82a5891c,0x4659c7b0,0x73dc0ca8,0xdad3aca2,0x00c74c7e,0x9a2521e2,0xf38eb6aa,0x64711ab6,0x5823150a,0xd13a3a9a,0x30a5aa04,0x0fb9a1da,0xef785119,0xc9f0b067,0x1e7dde42,0xdda4a7b2,0x1a1c2640,0x297c0633,0x744edb48,0x19adce93};

    // linear
	public static int f(int x, int bits) {
		int res = 0;
		for (int i = 0; i<bits; i++) {
			res = (res << 1) + (Long.bitCount(linear[i] & x) & 1);
		}
		return res;
	}

    private static final int[] exponential = {0x5e19b580,0x2b8f2f46,0x01dbee88,0x178439ae,0xe8b8434d,0x45fa4636,0xbb9c5c8c,0x5bdd6e67,0x930ae839,0x36528b7f,0x4fca205e,0xc50b7622,0xb0a63706,0x93ed56cf,0x81852045,0x21b5e7b9,0x16bbb5a7,0xb4837ca5,0xbd49dc89,0xf75c59ca,0x8e11761b,0xf84d7199,0x39e3ef49,0x9e4a936a,0x8d3842f1,0xf499e83d,0xd1431416,0xaca6d6ca,0x38582a69,0xe32a7dc3,0x2faf957e,0xa766a21e};

    // Exponential
	public static int hash(int x) {
		for (int value = 0; value<exponential.length; value++) {
			int dot = Long.bitCount(exponential[value] & x) & 1;
			if (dot!=0) return value+1;
		}
		return exponential.length;
	}
}