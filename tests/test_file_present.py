import unittest
import os
import io
import sys
#sys.path.insert(1, '../')
from build_data_file import *

class ImportTestCase(unittest.TestCase):
    def test_files_load_csvs_count_nr_loaded_csv_should_be_2(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        files = load_csvs(paths)
        assert len(files) == 19

    def test_noncsv_files_gives_error_message_and_exit(self):
        inv_paths = os.path.join(os.getcwd(), 'tests', 'invalid_test_data')

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        load_csvs(inv_paths)
        sys.stdout = sys.__stdout__
        print(capturedOutput.getvalue())

    def test_import_OSeMOSYS_param_files_to_outPutFile_hej_hej(self):
        path = os.path.join(os.getcwd(),'tests', 'hej_hej.txt')
        text = make_outputfile(path)
        assert text == "hej\nhej"

    def test_TRLV_3_operational_life_should_be_60(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = operational_life(outPutFile, dict_df['GIS_data'],  dict_df['input_data'], dict_df['operational_life'])
        test = "region\tTRLV_3\t60\n"
        assert test in outPutFile

    def test_MG_5_fixed_cost_should_be_1_in_2027(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = fixedcost(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['fixed_cost'])
        test = "region\tMG_5\t2027\t1.000000\n"
        assert test in outPutFile

    def test_SO_3_emissions_should_be_5_CO2_modeoperation_2_in_2027(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = emissionactivity(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['emissions'])
        test = "region\tSO_3\tCO2\t2\t2027\t5.000000\n"
        assert test in outPutFile

    def test_total_annual_limit_SO_5_should_be_3000(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = totaltechnologyannualactivityupperlimit(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['total_annual_technology_limit'])
        test = "region\tSO_5\t2027\t3000.000000\n"
        assert test in outPutFile

    def test_specifiedannualdemand_EL3_3_7_2025(self):
        paths = os.path.join(os.getcwd(),'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = specifiedannualdemand(outPutFile, dict_df['demand'], dict_df['input_data'])
        test = "region\tEL3_3\t2025\t7.000000\n"
        assert test in outPutFile

    def test_capital_cost_dynamic_WI_5_Capital_cost_should_be_1824_748531_2025(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                             dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'], dict_df['input_data'])
        test = "region\tWI_5\t2025\t1824.748531\n"
        assert test in outPutFile

    def test_capital_cost_dynamic_SOMG_3_Captial_cost_should_be_1390(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                             dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'], dict_df['input_data'])
        test = "region\tSOMG_3\t2025\t1390.723390\n"
        assert test in outPutFile

    def test_capital_cost_dynamic_SOPV_1_Captial_cost_should_be_(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                             dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'],dict_df['input_data'])
        test = "region\tSOPV_1\t2035\t1366.680000\n"
        assert test in outPutFile

    def test_capital_cost_dynamic_SOPV8h_3_Captial_cost_should_be_3338(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                             dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'],dict_df['input_data'])
        test = "region\tSOPV_8h_3\t2035\t3338.426341\n"
        assert test in outPutFile

    def test_capital_cost_dynamic_SOMG13h_2_Captial_cost_should_be_3062_2040(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capitalcost_dynamic(dict_df['GIS_data'], outPutFile, dict_df['capitalcost_RET'],
                                             dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'], dict_df['input_data'])
        test = "region\tSOMG_13h_3\t2040\t3843.294254\n"
        assert test in outPutFile

    def test_capital_cost_TRHV_5_should_be_(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capitalcost(outPutFile, dict_df['capitalcost'], dict_df['input_data'])
        test = "region\tTRLV_5\t2025\t5109.867698\n"
        assert test in outPutFile

    def test_capacitytoactivity_WI_5_is_31_536(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capacitytoactivity(dict_df['capacitytoactivity'], outPutFile, dict_df['input_data'])
        test = "region\tWI_5\t31.536000\n"
        assert test in outPutFile

    def test_inputact_TRLV_3_EL2_3_should_be_1_2025(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = inputact(outPutFile, dict_df['inputactivity'], dict_df['input_data'])
        test = "region\tTRLV_3\tEL2_3\t1\t2025\t1.000000\n"
        assert test in outPutFile

    def test_outputact_SOMG_5_EL2_5_should_be_1_modeop_1_2025(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = outputactivity(outPutFile, dict_df['outputactivity'], dict_df['input_data'])
        test = "region\tSOMG_3\tEL2_3\t1\t2025\t0.867500\n"
        assert test in outPutFile

    def test_specifiedannualdemand_EL3_4_is_2_41(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = specifiedannualdemand(outPutFile, dict_df['demand'], dict_df['input_data'])
        test = "region\tEL3_4\t2025\t2.410610\n"
        assert test in outPutFile

    def test_variable_cost_WI_5_scould_be_5(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = variblecost(dict_df['GIS_data'], outPutFile, dict_df['input_data'], dict_df['variable_cost'])
        test = "region\tWI_5\t1\t2025\t5.000000\n"
        assert test in outPutFile

    def test_specifieddemandprofile_EL3_10E_is_0_01756(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = SpecifiedDemandProfile(outPutFile, dict_df['demandprofile'], dict_df['input_data'])
        test = "region\tEL3\t10E\t2025\t0.017560\n"
        assert test in outPutFile

    def test_capacityfactor_solar_battery_SOPV_8h_3_1E_should_be_0_721543(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capacityfactor(outPutFile, dict_df['GIS_data'],
                                               dict_df['battery'], dict_df['input_data'], dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'])
        test = "region\tSOPV_8h_3\t1E\t2025\t0.721543\n"
        assert test in outPutFile

    def test_capacityfactor_solar_SOPV_5_should_be_0(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capacityfactor(outPutFile, dict_df['GIS_data'],
                                               dict_df['battery'], dict_df['input_data'], dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'])
        test = "region\tSOPV_5\t1N\t2030\t0.000000\n"
        assert test in outPutFile

    def test_capacityfactor_solar_SOPV_2_should_be_0_402357(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capacityfactor(outPutFile, dict_df['GIS_data'],
                                               dict_df['battery'], dict_df['input_data'], dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'])
        test = "region\tSOPV_2\t1D\t2030\t0.402357\n"
        assert test in outPutFile

    def test_capacityfactor_solar_WI_5_should_be_0_0471504(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capacityfactor(outPutFile, dict_df['GIS_data'],
                                               dict_df['battery'], dict_df['input_data'], dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'])
        test = "region\tWI_5\t1N\t2030\t0.045699\n"
        assert test in outPutFile

    def test_capacityfactor_solar_WI_13h_5_should_be_0_0471504(self):
        paths = os.path.join(os.getcwd(), 'tests','data')
        dict_df = load_csvs(paths)
        path = os.path.join(os.getcwd(), 'tests','osemosys_shell_param.txt')
        outPutFile = make_outputfile(path)
        outPutFile = capacityfactor(outPutFile, dict_df['GIS_data'],
                                               dict_df['battery'], dict_df['input_data'], dict_df['capacityfactor_wind'], dict_df['capacityfactor_solar'])
        test = "region\tWI_13h_5\t1N\t2020\t0.061989\n"
        assert test in outPutFile

if __name__ == '__main__':
    unittest.main()
