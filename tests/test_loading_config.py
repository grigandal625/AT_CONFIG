from at_config.core.at_config_loader import load_config
import yaml
import pytest

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_load_config():
    data = yaml.safe_load("""
    auth_token: default
    config:
        ATSolver: # конфигурация АТ-РЕШАТЕЛЯ
            kb:
                component: ATKrlEditor
                method: get_kb
                method_args: {'id': 5}
        ATTemporalSolver: # конфигурация темпорального решателя
            kb:
                path: /src/knowledge_base.xml # Файл БЗ
        ATSimulationMocking: # конфигурация заглушки подсистемы ИМ
            sm_run:
                path: /src/sm_run.xml # файл прогона ИМ
        ATJoint: # конфигурация компонента поддержки совместного функционирования
            at_simulation: ATSimulationMocking # имя компонента для отправки сообщений, предназначенных подсистеме ИМ (по умолчанию ATSimulation)
            at_simulation_process: 1
    """)

    result = await load_config(data.get('config'))
    assert result is not None
    assert result['ATSolver'].items['kb'].component == 'ATKrlEditor'
    assert result['ATSolver'].items['kb'].method == 'get_kb'
    assert result['ATSolver'].items['kb'].method_args == {'id': 5}
    assert result['ATTemporalSolver'].items['kb'].path == '/src/knowledge_base.xml'
    assert result['ATSimulationMocking'].items['sm_run'].path == '/src/sm_run.xml'
    assert result['ATJoint'].items['at_simulation'].data == 'ATSimulationMocking'
    assert result['ATJoint'].items['at_simulation_process'].data == 1