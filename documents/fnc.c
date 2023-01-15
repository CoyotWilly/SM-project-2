/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
// PID controller creation instance
arm_pid_instance_f32 PID_controller;

//duty saturation in range(0,1000)
void saturation(uint32_t duty_value){
	if (duty_value > WINDUP_UB){
		duty = 1000;
	}else if (duty_value < WINDUP_LB) {
		duty = 0;
	}
}

float absf(float value){
	if (value > 0.0){
		return value;
	}else if (value < 0.0){
		return value * -1;
	}
	return 0.0;
}
/* USER CODE END 0 */
