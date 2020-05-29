from spaceone.inventory.libs.manager import AWSManager


# todo: __init__에서 한번에 명세 할수 있게 바꾸기
# 지금은 로케이터에서 글로벌에서 값을 가져오는 로직 때문에 별도 파일이 없으면 에러 발생

class RDSConnectorManager(AWSManager):
    connector_name = 'RDSConnector'
