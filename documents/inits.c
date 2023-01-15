 /* USER CODE BEGIN 2 */
//   temperature sensor initialization
  BMP280_Init(&hi2c1, BMP280_TEMPERATURE_16BIT, BMP280_STANDARD, BMP280_FORCEDMODE);

  //UART interrupts initialization
  HAL_UART_Receive_IT(&huart2, (uint8_t*)input, 4);

//  Timer start for PWM generation and PID control logic
  HAL_TIM_Base_Start_IT(&htim2);
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);

//  LET THE FORCE BE WITH YOU mode start
  HAL_ADC_Start_IT(&hadc1);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
