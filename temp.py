        col1, col2, col3 = st.columns([1, 1, 1])

        if 'stock_id_count' not in st.session_state:
            st.session_state.stock_id_count = 0 
        if 'run_id_count' not in st.session_state:
            st.session_state.run_id_count=0

        with col1:
            year= st.text_input("Input Year", key='year_input')

        with col2:
            stock_id=st.text_input("Input Stock Id",key='stock_id_input')

        with col3:
            run_id = st.text_input("Input Run Id", key="run_number_input")
            run_id = str(run_id)         
        # Radio buttons for forecasting options
        # forecast_option = st.radio("Forecast Options", ("Forecast at the end of SeedTrain", "Forecast at the end of N-1", "Forecast at the end of N-2"))
        pg=Postgres_API()
        st.session_state.stock_id_count= pg.count_stock_id(stock_id,year)
        stock_id_count=st.session_state.stock_id_count
        st.session_state.run_id_count = pg.count_run_id_for_year(run_id,year)
        run_id_count_year= st.session_state.run_id_count
        st.text(f"Number of entries present for stock {stock_id}: {stock_id_count}")

        if stock_id_count==3:
            st.warning(f"There are already 3 entries present for {stock_id} in Year {year}. You can not add more.")
        if run_id_count_year==1:
            st.warning(f"The entered Run_id-{run_id} already exist for the given year-{year}.")

        if site==1:        
            if stock_id_count == 0:
                batch_value=1
                num_stages=7
            elif stock_id_count ==1 :
                batch_value=2
                num_stages=9
            else:
                batch_value=3
                num_stages=11
        else:
            if stock_id_count == 0:
                batch_value=1
                num_stages=8
            elif stock_id_count ==1 :
                batch_value=2
                num_stages=9
            else:
                batch_value=3
                num_stages=10

    
        total_stages_seed = get_total_seed_stages(site, batch_value,year)

        # Accordion for stage-wise user inputs
        with st.expander(f"2A. SeedTrain (0/{total_stages_seed})"):
            if "seed_values" not in st.session_state:
                st.session_state["seed_values"] = {}
            # User inputs for Seed Stage
            last_filled_stage = 100
            final = 112 if site == 1 else 111
            for day in range(101,final):  # Modify the range as needed
                if site == 1:
                    if batch_value == 1 and day in [105, 106, 107, 108]:
                        st.session_state.seed_values[f"seed_vcd_{day}"] = None
                        st.session_state.seed_values[f"seed_viab_{day}"] = None
                        continue
                    if batch_value == 2 and day in [107, 108]:
                        st.session_state.seed_values[f"seed_vcd_{day}"] = None
                        st.session_state.seed_values[f"seed_viab_{day}"] = None
                        continue
                else:
                    if batch_value == 1 and day in [105, 106]:
                        st.session_state.seed_values[f"seed_vcd_{day}"] = None
                        st.session_state.seed_values[f"seed_viab_{day}"] = None
                        continue
                    if batch_value == 2 and day in [106]:
                        st.session_state.seed_values[f"seed_vcd_{day}"] = None
                        st.session_state.seed_values[f"seed_viab_{day}"] = None
                        continue
                stage_name = get_seed_stage_name(site, day)
                st.markdown(f"##### {stage_name}")
                col1, col2 = st.columns(2)
                with col1:
                    seed_vcd_key = f"seed_vcd_{day}"
                    vcd_value = st.text_input(f"VCD (cells/mL) :", key=f"seed_vcd_{day}")
                    if vcd_value != "":
                        if is_float(vcd_value):
                            st.session_state.seed_values[f"seed_vcd_{day}"] = vcd_value
                        else:
                            # st.session_state.seed_values[f"seed_vcd_{day}"] = ""
                            st.error("Please enter a valid float value for VCD.")
                    # st.session_state.seed_values[f"seed_vcd_{day}"] = st.text_input(f"VCD :", key=f"seed_vcd_{day}")
                with col2:
                    seed_viab_key = f"seed_viab_{day}"
                    viab_value = st.text_input(f"Viability :", key=f"seed_viab_{day}")
                    if viab_value != "":
                        if is_float(viab_value):
                            st.session_state.seed_values[f"seed_viab_{day}"] = viab_value
                        else:
                            # st.session_state.seed_values[f"seed_viab_{day}"] = ""
                            st.error("Please enter a valid float value for Viability.")
                    # st.session_state.seed_values[f"seed_viab_{day}"] = st.text_input(f"Viability :", key=f"seed_viab_{day}")
                    # st.session_state.seed_values[f"seed_vcd_{day}"] = None
                    # st.session_state.seed_values[f"seed_viab_{day}"] = None
                if vcd_value != "" and viab_value != "":
                    last_filled_stage = day
            st.session_state.seed_values[f"seed_Stage_duration"] = st.text_input(f"Stage Duration(hrs) :", key=f"seed_Stage_duration")