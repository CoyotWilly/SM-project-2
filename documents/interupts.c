/* USER CODE BEGIN 4 */
// CONST measurement and data sending every 1s
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
	if (htim->Instance == TIM2){
		BMP280_ReadTemperatureAndPressure(&temperature, &pressure);
		if (force_control[0] == 1){
			HAL_ADC_Start_IT(&hadc1);
		} else {
			error = absf(temp_requested - temperature);
			if (error == 0.0){
				duty = 0;
			}else {
				duty = (uint32_t) 100 * arm_pid_f32(&PID_controller, error);
			}
		}
		saturation(duty);

		//UART data sending for logging
		snprintf(text, sizeof(text), "{\"temperature\":\"%.2f\",\"ref\":\"%.2f\",\"u\":\"%.f\",\"error\":\"%.4f\"}\n\r", temperature, temp_requested,(float) 0.1 * duty, error);
		HAL_UART_Transmit(&huart2, (uint8_t*)text, strlen(text), 1000);
		text[0] = 0;

		__HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, duty);
	}
}

// set temperature via UART implementation
void HAL_UART_RxCpltCallback ( UART_HandleTypeDef * huart ){
	float given = 0.01 * atof(input);

	if (given > 99.985){
		if (force_control[0] == 1){
			force_control[0] = 0;
		}else{
			force_control[0] = 1;
		}
	}else if (given > 0.0){
		temp_requested = given;
	}

	HAL_UART_Receive_IT(&huart2, (uint8_t*)input, 4);
}

// distance based control of PWM duty [LET THE FORCE BE WITH YOU MODE]
void HAL_ADC_ConvCpltCallback ( ADC_HandleTypeDef * hadc ){
	HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);

	float AdcValue = HAL_ADC_GetValue(&hadc1);

	AdcValue /=  1000;
	distance = 27.82 * powf(AdcValue, -1.081);

	duty = distance * 25;
	saturation(duty);
}
/* USER CODE END 4 */