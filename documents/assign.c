  /* USER CODE BEGIN 1 */
	//PID gains assignment
	PID_controller.Kp = PID_KP;
	PID_controller.Ki = PID_KI;
	PID_controller.Kd = PID_KD;

	//PID Init
	arm_pid_init_f32(&PID_controller, 1);
  /* USER CODE END 1 */
