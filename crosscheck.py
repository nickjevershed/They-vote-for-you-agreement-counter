import requests
import simplejson as json
import csv
from datetime import date, timedelta, datetime
import os

OA_KEY = os.environ['OA_THEYVOTEFORYOU']


divisionIds = [3006, 3005, 3004, 3003, 3002, 3016, 3015, 3014, 3013, 3012, 3011, 3010, 3009, 3008, 3007, 3032, 3031, 3030, 3029, 3035, 3034, 3033, 3036, 3038, 3037, 3080, 3079, 3078, 3077, 3076, 3075, 3074, 3073, 3083, 3082, 3081, 3085, 3084, 3088, 3087, 3086, 3152, 3153, 3155, 3154, 3157, 3156, 3158, 3163, 3162, 3161, 3160, 3159, 3168, 3167, 3166, 3165, 3164, 3173, 3172, 3171, 3170, 3169, 3174, 3180, 3179, 3178, 3177, 3176, 3175, 3182, 3181, 3188, 3187, 3191, 3190, 3202, 3201, 3200, 3199, 3198, 3205, 3204, 3203, 3223, 3222, 3221, 3220, 3225, 3224, 3239, 3236, 3235, 3234, 3233, 3232, 3231, 3246, 3245, 3244, 3243, 3242, 3241, 3264, 3263, 3262, 3520, 3283, 3282, 3281, 3280, 3279, 3278, 3277, 3276, 3292, 3291, 3290, 3289, 3300, 3299, 3298, 3297, 3296, 3295, 3294, 3293, 3307, 3306, 3305, 3304, 3303, 3302, 3301, 3318, 3317, 3316, 3315, 3314, 3313, 3312, 3311, 3310, 3309, 3308, 3337, 3336, 3335, 3334, 3333, 3332, 3331, 3330, 3329, 3328, 3327, 3344, 3343, 3342, 3341, 3340, 3339, 3372, 3371, 3539, 3538, 3537, 3536, 3535, 3534, 3533, 3532, 3531, 3530, 3529, 3528, 3527, 3526, 3525, 3524, 3370, 3369, 3368, 3367, 3366, 3365, 3364, 3363, 3362, 3361, 3360, 3359, 3358, 3357, 3356, 3355, 3380, 3383, 3389, 3388, 3387, 3386, 3385, 3407, 3406, 3405, 3404, 3418, 3417, 3416, 3415, 3414, 3413, 3412, 3411, 3421, 3420, 3419, 3547, 3546, 3545, 3544, 3543, 3430, 3429, 3428, 3427, 3426, 3425, 3435, 3434, 3433, 3432, 3431, 3440, 3439, 3438, 3447, 3446, 3445, 3444, 3443, 3442, 3441, 3456, 3455, 3454, 3453, 3452, 3451, 3450, 3449, 3459, 3458, 3457, 3463, 3462, 3461, 3565, 3564, 3563, 3562, 3561, 3560, 3573, 3572, 3571, 3570, 3569, 3568, 3581, 3580, 3579, 3578, 3577, 3576, 3575, 3574, 3583, 3582, 3598, 3597, 3596, 3595, 3594, 3593, 3592, 3591, 3590, 3589, 3588, 3587, 3586, 3585, 3584, 3609, 3608, 3607, 3606, 3605, 3604, 3603, 3602, 3601, 3611, 3610, 3624, 3623, 3622, 3621, 3620, 3619, 3625, 3629, 3628, 3627, 3626, 3636, 3635, 3634, 3633, 3632, 3631, 3630, 3646, 3645, 3644, 3643, 3642, 3665, 3664, 3663, 3662, 3661, 3660, 3658, 3657, 3656, 3655, 3654, 3653, 3652, 3651, 3650, 3649, 3648, 3647, 3670, 3669, 3668, 3667, 3680, 3679, 3678, 3677, 3676, 3675, 3682, 3687, 3686, 3685, 3684, 3683, 3701, 3700, 3699, 3698, 3697, 3706, 3705, 3704, 3703, 3702, 3708, 3707, 3711, 3712, 3717, 3716, 3715, 3714, 3721, 3720, 3719, 3718, 3732, 3731, 3730, 3729, 3728, 3727, 3726, 3725, 3724, 3736, 3735, 3734, 3751, 3750, 3749, 3748, 3747, 3746, 3745, 3744, 3743, 3742, 3741, 3740, 3739, 3738, 3767, 3766, 3765, 3764, 3763, 3762, 3761, 3760, 3759, 3758, 3757, 3756, 3768, 3769, 3779, 3778, 3777, 3776, 3775, 3774, 3783, 3782, 3781, 3780, 3800, 3799, 3798, 3797, 3807, 3806, 3805, 3804, 3803, 3802, 3801, 3900, 3899, 3898, 3897, 3896, 3895, 3894, 3893, 3819, 3818, 3817, 3816, 3815, 3829, 3828, 3827, 3826, 3825, 3824, 3823, 3838, 3837, 3836, 3835, 3834, 3833, 3832, 3831, 3830, 3848, 3847, 3846, 3845, 3844, 3868, 3867, 3866, 3865, 3864, 3863, 3862, 3861, 3860, 3859, 3858, 3857, 3856, 3855, 3870, 3869, 3876, 3875, 3874, 3873, 3872, 3892, 3891, 3879, 3878, 3877, 3885, 3884, 3883, 3882, 3881, 3880, 3889, 3888, 3887, 3901, 3907, 3910, 3909, 3908, 3916, 3915, 3914, 3913, 3922, 3921, 3920, 3919, 3928, 3927, 3930, 3929, 3933, 3932, 3931, 3941, 3940, 3939, 3938, 3937, 3936, 3935, 3934, 3949, 3948, 3947, 3946, 3945, 3944, 3943, 3942, 3958, 3957, 3956, 3955, 3963, 3962, 3961, 3960, 3959, 3971, 3970, 3969, 3968, 3967, 3966, 3965, 3964, 3973, 3972, 3979, 3978, 3983, 3982, 3981, 3992, 3991, 3990, 3989, 3988, 3987, 3986, 3985, 3996, 3995, 3994, 4005, 4004, 4003, 4002, 4010, 4009, 4008, 4007, 4006, 4014, 4013, 4012, 4029, 4028, 4027, 4026, 4047, 4046, 4045, 4044, 4043, 4042, 4041, 4040, 4039, 4038, 4053, 4052, 4051, 4050, 4049, 4048, 4062, 4061, 4060, 4059, 4084, 4083, 4082, 4081, 4080, 4079, 4092, 4091, 4090, 4089, 4099, 4098, 4097, 4096, 4095,4104, 4103, 4102, 4101]


with open('cross-check-output.csv', 'w') as csvoutput:
	writer = csv.writer(csvoutput, lineterminator='\n')
	writer.writerow(['division','xenophon','lazaraus'])

	for id in divisionIds:
		print "Original division at ", 'https://theyvoteforyou.org.au/api/v1/divisions/{id}.json?key={key}'.format(id=id,key=OA_KEY)
		fileLoc = 'votejson/{id}.json'.format(id=id)
		with open(fileLoc,'r') as jsonFile:
			votes = json.load(jsonFile)
			newrows = []
			senatorsPresent = []
			newrows.append(id)
			for vote in votes['votes']:
				# print vote
				senatorsPresent.append(vote['member']['person']['id'])

			#Check if Xenophon present
			
			if 10717 in senatorsPresent:
				print "Xenophon present"

				for vote in votes['votes']:
					if vote['member']['person']['id'] == 10717:
						newrows.append(vote['vote'])
						
			else:
				print "Xenophon absent"
				newrows.append("")			

			#Check if Lazarus present
			
			if 10831 in senatorsPresent:
				print "Lazarus present"

				for vote in votes['votes']:
					if vote['member']['person']['id'] == 10831:
						newrows.append(vote['vote'])
						
			else:
				print "Lazarus absent"
				newrows.append("")

			writer.writerow(newrows)			