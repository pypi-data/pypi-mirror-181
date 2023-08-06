# -*- coding: utf-8 -*-

"""
BGE 私有平台 SDK 客户端模块。

使用示例：

"""
import json

from . import constants
from . import models
from .error import BGEError
from .http import HTTPRequest
from .utils import make_sign

from weakref import ref

__all__ = ['PrivateAPI', 'endpoints']

endpoints = [v['endpoint'] for v in constants.ENDPOINTS]


class PrivateAPI(object):
    """

    Args:
        app_key (字符串): 第三方客户端 client_id；
        app_secret (字符串): 第三方客户端 client_secret；
        endpoint (字符串, 非必填): 平台对外服务的访问域名，
                                 默认值为 https://api.private.omgut.com；
        max_retries (数字, 非必填): 接口请求重试次数，默认值为 3；
        timeout (数字, 非必填): 接口请求默认超时间，默认值为 None；
        verbose (布尔, 非必填)：输出测试日志，默认值为 False；
    """

    def __init__(self, app_key, app_secret, endpoint=None, max_retries=None,
                 timeout=None, verbose=False):
        self.app_key = app_key
        self.app_secret = app_secret
        if endpoint is None:
            endpoint = constants.DEFAULT_ENDPOINT
        self.endpoint = endpoint
        if max_retries is not None:
            max_retries = int(max_retries)
        self.max_retries = max_retries
        if timeout is not None:
            timeout = int(timeout)
        self.timeout = timeout
        self.verbose = verbose
        self.account = Account(self)
        self.report = Report(self)

    def get_user(self, **kwargs):
        """获取用户信息

        Returns:
            Model: 用户数据；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose
        )
        result = request.post(
            '/openbge/user/profile', data=data, timeout=timeout)
        return models.Model(result)

    def get_samples(self, **kwargs):
        """查询一个或多个样品

        biosample_id与 external_sample_id 须且提供其中之一；

        Args:
            biosample_id(str, 非必填): 样品编号，多个样品用','隔开；
            external_sample_id(str, 非必填): 扩展生产样品编号，多个编号以','隔开；
            page(int, 非必填): 当前页码，默认为 1；
            limit(int, 非必填)： 一页最大返回数据量，默认为 50；

        Returns:
            Model: 样品数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose
        )
        result, pagination = request.post(
            '/openbge/samples', data=data, timeout=timeout)
        ret = {}
        ret['count'] = count = pagination['count']
        next_page = pagination['page'] + 1
        if count == 0:
            next_page = None
        ret['next_page'] = next_page
        ret['total'] = pagination['total']
        ret['result'] = [models.Model(item) for item in result]
        return ret

    def get_samples_external_ids(self,
                                 biosample_site,
                                 project_id,
                                 external_ids):
        """获取样品外部编号"""
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            biosample_site=biosample_site,
            project_id=project_id,
            external_ids=external_ids
        )
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose
        )
        result = request.post(
            '/openbge/samples/external_ids', data=data, timeout=timeout)
        ret = [models.Model(item) for item in result]
        return ret

    def register_sample(self, biosample_site, project_id, **kwargs):
        """注册样品

        Args:
            biosample_site(int): 采样部位；
            project_id(str): 项目编号；
            **kwargs: 其他非必填参数；

        Returns:
            Model: 样品数据，包含生物样品编号;
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, biosample_site=biosample_site,
            project_id=project_id, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose
        )
        result = request.post(
            '/openbge/samples/register', data=data, timeout=timeout)
        return models.Model(result)

    def improve_sample(self, biosample_id, **kwargs):
        """补充已注册的生物样品中未被赋值的信息

        已赋值的数据无法变更；如果提供不同的值，将报错；如果提供与已保存数据相同的值，
        接口正常返回;

        Args:
            biosample_id(str): 生物样品编号
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, biosample_id=biosample_id,
            **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/samples/improve', data=data, timeout=timeout)
        if result is None:
            result = {'biosample_id': biosample_id}
            result.update(kwargs)
        return models.Model(result)

    def variant(self, biosample_id, rsids):
        """查询变异位点数据

        Args:
            biosample_id(str): 生物样品编号
            rsids(str): rsid，多个 rsid 通过 ',' 分隔；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, biosample_id=biosample_id,
            rsids=rsids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/v2/openbge/genome/variant', data=data, timeout=timeout)
        ret = [models.Model(item) for item in result]
        return ret

    def variant_v1(self, biosample_id, **kwargs):
        """旧版变异位点查询接口

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, biosample_id=biosample_id,
            **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/genome/variant', data=data, timeout=timeout)
        ret = [models.Model(item) for item in result]
        return ret

    def professional_variant(self, biosample_id, only_variant_site=True,
                             regions=None, bed_file=None):
        """查询专业级变异数据

        regions 与 bed_file 须且提供其中之一

        Args:
            biosample_id(str): 生物样品编号；
            only_variant_site(bool): 是否仅输出变异位置，默认为True；
            regions(str): 需要抽取区域的坐标数据，数组长度不得超过5000；
            bed_file(str): 需要抽取区域的 bed 文件路径，文件须为 zip 压缩文件
                           且内容不得超过 100w 行

        Returns:
            异步任务id
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        if regions is not None and bed_file is not None:
            raise BGEError(
                'regions and bed_ File needs to provide one of them')
        if regions is None and bed_file is None:
            raise BGEError(
                'Regions and bed_ File cannot be provided at the same time')
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose,
            content_type=None)
        if regions is not None:
            data = make_sign(
                self.app_key, self.app_secret, biosample_id=biosample_id,
                only_variant_site=only_variant_site, regions=regions)
            files = None
        else:
            files = {'bed_file': open(str(bed_file), 'rb')}
            data = make_sign(
                self.app_key, self.app_secret, biosample_id=biosample_id,
                only_variant_site=only_variant_site)
        result = request.post(
            '/openbge/professional/variant', data=data, files=files,
            timeout=timeout)
        return models.Model(result)

    def get_origin_taxon_abundance(self, biosample_id, taxon_ids=None,
                                   next_page=None, limit=50, **kwargs):
        """获取类群丰度

        Args:
            biosample_id(str): 生物样品编号；
            taxon_ids(str, 非必填）： BGE 物种编号，多个以','隔开；
            next_page(int, 非必填）: 当前页码，默认值为 1;
            limit(int, 非必填）: 每页数量，默认为 50；

        Returns:
            类群丰度数据详情；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'biosample_id': biosample_id,
            'taxon_id': taxon_ids,
            'limit': limit
        })
        page = 1
        if next_page is not None:
            page = next_page
        kwargs['page'] = page
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result, pagination = request.post(
            '/openbge/microbiome/taxon_abundance', data=data,
            timeout=timeout)
        return result, pagination

    def get_taxon_abundance(self, biosample_id, taxon_ids=None,
                            next_page=None, limit=50, **kwargs):
        """获取类群丰度

        Args:
            biosample_id(str): 生物样品编号；
            taxon_ids(str, 非必填）： BGE 物种编号，多个以','隔开；
            next_page(int, 非必填）: 当前页码，默认值为 1;
            limit(int, 非必填）: 每页数量，默认为 50；

        Returns:
            类群丰度数据详情；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'biosample_id': biosample_id,
            'taxon_id': taxon_ids,
            'limit': limit
        })
        page = 1
        if next_page is not None:
            page = next_page
        kwargs['page'] = page
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result, pagination = request.post(
            '/openbge/microbiome/taxon_abundance', data=data,
            timeout=timeout)
        ret = {}
        ret['count'] = count = pagination['count']
        next_page = pagination['page'] + 1
        if count == 0:
            next_page = None
        ret['next_page'] = next_page
        ret['result'] = result
        return ret

    def get_func_abundance(self, biosample_id, catalog, ids=None,
                           limit=50, next_page=None, **kwargs):
        """获取功能丰度

        Args:
            biosample_id(str): 生物样品编号；
            catalog(str): 目录标签，可选值为：go、ko、eggnog、pfam、kegg-pwy、
                           kegg-mdl、level4ec、metacyc-rxn、metacyc-pwy；
            ids (str, 非必填): BGE物种功能编号，多个值以逗号隔开；
            limit (int, 非必填): 一页返回数量，默认值为 50；
            next_page (str, 非必填): 下一页，用于获取下一页数据；

        Returns:
            Model: 功能丰度数据详情；
        """
        kwargs.update({
            'biosample_id': biosample_id,
            'catalog': catalog,
            'ids': ids,
            'next_page': next_page,
            'limit': limit
        })
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/microbiome/func_abundance', data=data,
            timeout=timeout)
        return result

    def get_gene_abundance(self, biosample_id, catalog, data_type, ids=None,
                           limit=50, next_page=None, **kwargs):
        """获取基因丰度

        Args:
            biosample_id (str): 生物样品编号；
            catalog (str): 分类标签，可选值：IGC_9.9M、UniRef90_HUMAnN2_0.11；
            data_type (str): 返回数据类型，可选值：list、file；
            ids (str, 非必填): BGE 物种 IGC 基因编号，多个值以逗号分割，
                                    如：igc_50,igc_51；
            limit (int, 非必填): 一页最大返回数量，默认 50，最大值为 1000；
            next_page (str, 非必填): 接口返回的下一页参数；

        Returns:
            Model: 基因丰度数据详情；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'biosample_id': biosample_id,
            'catalog': catalog,
            'data_type': data_type,
            'ids': ids,
            'next_page': next_page,
            'limit': limit
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/microbiome/gene_abundance', data=data,
            timeout=timeout)
        return result

    def data_element_search(self, query, data_element_source_domains=None,
                            page=None, limit=50, types=None, **kwargs):
        """搜索数据元和数据集

        Args:
            query(str): 查询文本；
            data_element_source_domains(str): 数据元 source_domain，
                                              逗号分割多个 source_domain；
            page(int): 当前页；
            limit(int): 每页返回数量；
            types(str): 搜索的数据类型，取值范围：data_element、collection、
                        data_element,collection，不提供参数时默认搜索两种数据类型；
        Returns:
            id: 索引编号；
            app: 索引归属应用；
            type: 索引类型；
            highlight: 搜索高亮
            data: 索引数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'query': query,
            'data_element_source_domains': data_element_source_domains,
            'page': page,
            'limit': limit,
            'types': types
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_element/search', data=data, timeout=timeout)
        return models.Model(result)

    def get_data_element(self, data_element_id):
        """根据数据元编号获取数据元

        Args:
            data_element_id(str): 数据元编号；

        Returns:
            数据元
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, data_element_id=data_element_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_element/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def data_element_by_source(self, data_element_source_domain,
                               data_element_source_id):
        """根据数据来源获取数据元

        Args:
            data_element_source_domain(str): 数据元来源域；
            data_element_source_id(str): 数据元来源编号；

        Returns:
            数据元
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            data_element_source_domain=data_element_source_domain,
            data_element_source_id=data_element_source_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_element/retrieve/by_source', data=data,
            timeout=timeout)
        return models.Model(result)

    def batch_data_element_by_source(self, data_element_source_domain,
                                     data_element_source_ids):
        """根据数据来源获取多个数据元

        Args:
            data_element_source_domain(str): 数据元来源域；
            data_element_source_ids(str):  数据元来源编号,多个 id 用逗号隔开；

        Returns:
            数据元列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            data_element_source_domain=data_element_source_domain,
            data_element_source_ids=data_element_source_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_element/batch_retrieve/by_source', data=data,
            timeout=timeout)
        ret = {}
        ret['result'] = [models.Model(item) for item in result]
        return ret

    def replace_data_element(self, data_element_source_domain,
                             data_element_source_id, columns):
        """更新或创建一个数据元

        Args:
            data_element_source_domain(str): 数据元来源域；
            data_element_source_id(str): 数据元来源编号；
            columns(dict): 需要更新或创建的数据元属性；

        Returns:
            替换或更新后的数据元
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        columns = json.dumps(columns)
        data = make_sign(
            self.app_key, self.app_secret,
            data_element_source_domain=data_element_source_domain,
            data_element_source_id=data_element_source_id, columns=columns)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_element/replace', data=data, timeout=timeout)
        return models.Model(result)

    def discard_data_element(self, data_element_source_domain,
                             data_element_source_id):
        """废弃一个数据元

        Args:
            data_element_source_domain(str): 数据元来源域；
            data_element_source_id(str): 数据元来源编号；

        Returns:
            数据元编号
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            data_element_source_domain=data_element_source_domain,
            data_element_source_id=data_element_source_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_element/discard', data=data, timeout=timeout)
        return models.Model(result)

    def merge_data_element(self, data_element_ids, merge_data_element_id,
                           comment=None):
        """将一个或多个数据元合并到另一个数据元中

        Args:
            data_element_ids(str): 被合并的数据元编号，逗号分割多个；
            merge_data_element_id(str): 合并到的数据元编号；
            comment(str): 备注；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            data_element_ids=data_element_ids,
            merge_data_element_id=merge_data_element_id, comment=comment)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/openbge/data_element/merge', data=data, timeout=timeout)

    def retrieve_batch(self, batch_no):
        """获取批次详情

        Args:
            batch_no(int): 批次号；

        Returns:
            该批次的详情
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, batch_no=batch_no)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/batch/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def register_batch(self, **kwargs):
        """注册批次号

        Args:
            title(str, 非必填): 批次标题；
            intro(str, 非必填): 批次简介；

        Returns:
            注册好的批次号
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/batch/register', data=data, timeout=timeout)
        return models.Model(result)

    def import_batch(self, batch_no, data_items, biosample_id=None):
        """导入数据元数据

        Args:
            batch_no(int, 必填): 批次号；
            data_items(list，必填): 待导入的数据项列表；
            data_items.data_element_id(str, 必填): 数据元编号；
            data_items.attributes(dict, 必填): 数据元数据；
            biosample_id(str, 非必填): 生物样品编号；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, batch_no=batch_no,
            data_items=data_items, biosample_id=biosample_id)
        data = json.dumps(data)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose,
            content_type='application/json')
        request.post(
            '/openbge/batch/import', data=data, timeout=timeout)

    def commit_batch(self, batch_no):
        """推送该批次数据

        Args:
            batch_no(int): 批次号；

        Returns:
            推送该批次数据的任务详情
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, batch_no=batch_no)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/batch/commit', data=data, timeout=timeout)
        return models.Model(result)

    def retrieve_data_item(self, data_element_id, namespace,
                           biosample_id=None, batch_no=None):
        """获取单个数据项

        Args:
            data_element_id(str, 必填): 数据元编号；
            namespace(str, 必填): 命名空间；
            biosample_id(str, 非必填): 生物样品编号；
            batch_no(int, 非必填): 批次号；

        Returns:
            数据项
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, data_element_id=data_element_id,
            namespace=namespace, biosample_id=biosample_id,
            batch_no=batch_no)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_item/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def retrieve_batch_data_item(self, namespace, **kwargs):
        """获取多个数据项 V2

        Args:
            namespace(str): 命名空间；
            kwargs: 其他非必填参数；

        Returns:
            数据项列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'namespace': namespace
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/v2/openbge/data_item/batch_retrieve', data=data,
            timeout=timeout)
        result = models.Model(result)
        result['result'] = [models.Model(item) for item in result['result']]
        return result

    def data_item_query(self, namespace, **kwargs):
        """获取某个命名空间下的数据项列表

        Args:
            namespace(str): 命名空间；
            kwargs: 其他非必填参数；

        Returns:
            数据项列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'namespace': namespace
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_item/query', data=data, timeout=timeout)
        return models.Model(result)

    def data_item_change_list(self, namespace, **kwargs):
        """查询样品的数据项变更列表

        Args:
            namespace(str): 命名空间；
            kwargs: 其他非必填参数；

        Returns:
            数据发生变更过的数据元编号列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'namespace': namespace
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/data_item/change_list', data=data, timeout=timeout)
        return models.Model(result)

    def add_collection(self, collection_name, collection_type,
                       collection_omic, collection_description=None,
                       data_element_ids=None):
        """增加一个数据集，同时可给该数据集添加数据元和自动为该数据集添加索引

        Args:
            collection_name(str): 数据集名称；
            collection_type(str): 类型，取值范围：private、public；
            collection_omic(str): 组学，取值范围：multiomics、genomics、
                                  metagenomics、phenomics、exposomics
            collection_description: 数据集描述；
            data_element_ids(str): 数据元文件路径，文件中数据元编号之间以空格或换行隔开；

        Returns:
            数据集编号
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, collection_name=collection_name,
            collection_type=collection_type,
            collection_omic=collection_omic,
            collection_description=collection_description)
        files = None
        if data_element_ids:
            files = {'data_element_ids': open('data_element_ids', 'rb')}
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose,
            content_type=None)
        result = request.post(
            '/openbge/data_element_collection/add', data=data, files=files,
            timeout=timeout)
        return models.Model(result)

    def edit_collection(self, collection_id, data_element_ids=None,
                        **kwargs):
        """编辑数据集的相关属性，或覆盖数据集中的数据元

        Args:
            collection_id(str): 数据集编号；
            data_element_ids(str): 数据元文件路径；
            kwargs: 其他非必填参数；

        Returns:
            数据集编号
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'collection_id': collection_id
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose,
            content_type=None)
        files = None
        if data_element_ids:
            files = {'data_element_ids': data_element_ids}
        result = request.post(
            '/openbge/data_element_collection/edit', data=data, files=files,
            timeout=timeout)
        return models.Model(result)

    def collection_detail_or_delete(self, collection_id, type='detail'):
        """搜索数据集和该集合下的数据元 or 删除数据集并自动删除该集合的索引

        Args:
            collection_id(str): 数据集编号；
            type(str): 对数据集进行查询或删除操作，可选项 detail, delete；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, collection_id=collection_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        if type == 'detail':
            result = request.post(
                '/openbge/data_element_collection/collection_detail',
                data=data,
                timeout=timeout)
        elif type == 'delete':
            result = request.post(
                '/openbge/data_element_collection/delete', data=data,
                timeout=timeout)
        else:
            raise BGEError(
                'type: {} is not in the optional params range.'.format(
                    type))
        return models.Model(result)

    def stream_range(self, namespace, data_element_id, **kwargs):
        """根据数据流生成时间的范围查询数据流数据；

        Args:
            namespace(str): 命名空间；
            data_element_id(str): 数据元编号；
            kwargs: 其他非必填参数；

        Returns:
            数据元详情与数据流相关数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'namespace': namespace,
            'data_element_id': data_element_id
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/stream/range', data=data, timeout=timeout)
        return models.Model(result)

    def write_stream(self, fundamental_entity_id, data_element_id,
                     stream_generate_time, stream_data,
                     duplicate_enabled=None):
        """写入一条数据流数据；

        Args:
            fundamental_entity_id(str): 个体编号；
            data_element_id(str): 数据元编号；
            stream_generate_time(str): 流数据生成时间;
            stream_data(str): 流数据内容，JSON 格式内容；
            duplicate_enabled(str): 是否允许重复写入相同数据；

        Returns:
            数据流 id
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            fundamental_entity_id=fundamental_entity_id,
            data_element_id=data_element_id,
            stream_generate_time=stream_generate_time,
            stream_data=stream_data, duplicate_enabled=duplicate_enabled)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/stream/write', data=data, timeout=timeout)
        return models.Model(result)

    def batch_write_stream(self, streams, duplicate_enabled=None):
        """写入多条数据流数据；

        最多一次写入 100 条数据；

        Args:
            streams(list): 要写入的数据流数据数组；

        Returns:
            成功写入的数量，数据流和数据元相关数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        streams = json.dumps(streams)
        data = make_sign(
            self.app_key, self.app_secret, streams=streams,
            duplicate_enabled=duplicate_enabled)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/stream/batch_write', data=data, timeout=timeout)
        return models.Model(result)

    def stream_retrieve(self, stream_id):
        """获取一条数据流

        Args:
            stream_id(str): 数据流编号；

        Returns:
            数据流详情
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, stream_id=stream_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/stream/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def stream_bind(self, biosample_id):
        """获取样品所属个体编号

        Args:
            biosample_id(str): 生物样品编号；

        Returns:
            个体编号
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, biosample_id=biosample_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/stream/bind', data=data, timeout=timeout)
        return models.Model(result)

    def download_omics_data(self, namespace,
                            biosample_ids=None,
                            format='json'):
        """下载组学数据

        Args:
            namespace (str): 命名空间
            biosample_ids (str, optional): 样品编号；
            format (str, optional): 下载文件格式；

        Returns:
            file like object: 文件流对象
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            namespace=namespace,
            biosample_ids=biosample_ids,
            format=format
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        stream = request.post(
            '/datamall/omics_data/download',
            data=data,
            timeout=timeout
        )
        return stream

    def oauth2_application(self, client_id, redirect_uri):
        """获取客户端详情

        Args:
            client_id(str): 开放平台客户端 client_id；
            redirect_uri(str): 回调地址；

        Returns:
            应用详情和权限范围
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, client_id=client_id,
            redirect_uri=redirect_uri)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/oauth2/application', data=data, timeout=timeout)
        return models.Model(result)

    def oauth2_authorize(self, client_id, redirect_uri, auth_token,
                         biosample_ids=None):
        """获取用户授权

        Args:
            client_id(str): 开放平台客户端 client_id；
            redirect_uri(str): 回调地址；
            auth_token(str): 用户授权令牌；
            biosample_ids(str, 非必填): 选中的授权样品信息，json格式字符串

        Returns:
            用户授权 code
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, client_id=client_id,
            redirect_uri=redirect_uri, auth_token=auth_token,
            biosample_ids=json.dumps(biosample_ids))
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/oauth2/authorize', data=data, timeout=timeout)
        return models.Model(result)

    def oauth2_grants(self, auth_token, client_id=None):
        """获取授权列表

        Args:
            auth_token(str): 用户授权令牌；
            client_id(str, 非必填): 开放平台客户端 client_id；

        Returns:
            应用信息和套件信息
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, auth_token=auth_token,
            client_id=client_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/oauth2/grants', data=data, timeout=timeout)
        if result == []:
            return None
        return models.Model(result)

    def oauth2_revoke_grant(self, auth_token, client_id):
        """解除用户授权

        Args:
            auth_token(str): 用户授权令牌；
            client_id(str): 开放平台客户端 client_id；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, auth_token=auth_token,
            client_id=client_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/openbge/oauth2/revoke_grant', data=data, timeout=timeout)

    def get_surveys(self, **kwargs):
        """获取已创建的问卷

        Args:
            survey_ids(str, 非必填): 问卷 id，多个 id 以逗号分隔；
            developer_ids(str, 非必填): 开发者用户 id，多个 id 以逗号分隔；
            sort(str, 非必填): 以某字段排序，默认升序，字段前加上‘-’代表降序；
            page(int, 非必填): 当前页，默认为 1；
            limit(int, 非必填): 每页数量，默认为 50；

        Returns:
            问卷详情数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/surveys', data=data, timeout=timeout)
        return models.Model(result)

    def surveys_retrieve(self, survey_id):
        """根据问卷编号获取问卷

        Args:
            survey_id(int): 问卷 id；

        Returns:
            问卷详情
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, survey_id=survey_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/surveys/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def survey_replace(self, developer_id, title, description, redirect_url,
                       **kwargs):
        """如果参数中包含 survey_id 且 数据库中存在 survey_id 对应的问卷数据，
           则更新该问卷的数据； 否则，将根据参数创建一个新的问卷；

        Args:
            developer_id(str, 必填): 开发者 id；
            title(str, 必填): 标题；
            description(str, 必填): 问卷描述；
            redirect_url(str, 必填): 问卷填写完成后跳转地址；
            survey_id(int, 非必填): 问卷 id；
            end_text(str, 非必填): 结束语；

        Returns:
            更新或创建后的问卷数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'developer_id': developer_id,
            'title': title,
            'description': description,
            'redirect_url': redirect_url
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/surveys/replace', data=data, timeout=timeout)
        return models.Model(result)

    def survey_async(self, survey_id=None):
        """发布问卷
        Args:
            survey_id(int, 非必填): 问卷 id；

        Returns:
            任务 id
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, survey_id=survey_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/surveys/publish/async', data=data, timeout=timeout)
        return models.Model(result)

    def survey_delete(self, survey_ids):
        """删除问卷

        Args:
            survey_ids(str): 问卷 id，多个 id 用逗号隔开
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, survey_ids=survey_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/surveys/delete', data=data, timeout=timeout)

    def survey_question(self, survey_id, **kwargs):
        """根据参数筛选某问卷中的问题

        Args:
            survey_id(int, 必填): 问卷 id；
            question_ids(str, 非必填): 问题 id，多个 id 用逗号分隔
            data_element_identifier_des(str, 非必填): 数据元编号
            sort(str, 非必填): 以某字段排序，默认升序，字段前加上 “-” 代表降序；
            page(int, 非必填): 当前页，默认 1；
            limit(int, 非必填): 每页数量，默认为50；

        Returns:
            Model: 问题详细数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'survey_id': survey_id
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/questions', data=data, timeout=timeout)
        return models.Model(result)

    def questions_retrieve(self, question_id):
        """根据 id 获取问题详细数据

        Args:
            question_id(int): 问题 id；

        Returns:
            Model: 问卷编号与问题的详细数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, question_id=question_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/questions/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def questions_replace(self, survey_id, question_id, title,
                          data_element_identifier_de, **kwargs):
        """更新或创建问题

        Args:
            survey_id(int, 必填): 问卷 id；
            question_id(int, 必填): 问题 id；
            title(str, 必填): 问题标题；
            data_element_identifier_de(str, 必填): 数据元编号；
            qtype(str, 非必填): 问题类型；
            order(int, 非必填): 顺序号；
            required(str, 非必填): 是否必填；
            description(str, 非必填): 问题描述；

        returns:
            Model: 问卷 
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'survey_id': survey_id,
            'question_id': question_id,
            'title': title,
            'data_element_identifier_de': data_element_identifier_de
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/questions/replace', data=data, timeout=timeout)
        return models.Model(result)

    def questions_delete(self, question_ids):
        """删除一个或多个问题

        Args:
            question_ids(str): 问题 id，多个 id 用逗号分隔
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, question_ids=question_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/questions/delete', data=data, timeout=timeout)

    def questions_clean(self, survey_ids):
        """清空一个或多个问卷下的全部问题

        Args:
            survey_ids(str): 问卷 id，多个 id 用逗号分隔；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, survey_ids=survey_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/questions/clean', data=data, timeout=timeout)

    def survey_options(self, question_id, **kwargs):
        """根据参数筛选某个问题下的选项

        Args:
            question_id(int, 非必填): 问题 id；
            option_ids(str, 非必填): 选项 id，多个 id 用逗号分隔；
            sort(str, 非必填): 排序字段，字段前加上 “-” 代表降序；
            page(int, 非必填): 当前页，默认为 1；
            limit(int, 非必填): 每页数量，默认为 50；

        Returns:
            问题及问题下的可选项
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'question_id': question_id
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/options', data=data, timeout=timeout)
        return models.Model(result)

    def options_retrieve(self, option_id):
        """根据 id 获取选项

        Args:
            option_id(int): 选项 id；

        Returns:
            Model: 选项数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, option_id=option_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/options/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def options_replace(self, question_id, concept_code, value, **kwargs):
        """更新或创建一个新的选项

        Args:
            question_id(int, 必填): 问题 id；
            concept_code(str, 必填): 选项系统编码；
            value(str, 必填): 值；
            option_id(int, 非必填): 选项 id；
            order(int, 非必填): 顺序，默认为 0；

        Returns:
            Model: 更新或创建后的选项
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'question_id': question_id,
            'concept_code': concept_code,
            'value': value
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/options/replace', data=data, timeout=timeout)
        return models.Model(result)

    def options_delete(self, option_ids):
        """删除一个或多个选项

        Args:
            option_ids(str): 选项 id，多个 id 用逗号分隔；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, option_ids=option_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/options/delete', data=data, timeout=timeout)

    def options_clean(self, question_ids):
        """清空某些问题下的全部选项

        Args:
            question_ids(str): 问题 id，多个 id 用逗号分隔；  
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, question_ids=question_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/options/clean', data=data, timeout=timeout)

    def options_batch_create(self, question_id, options):
        """批量创建某问题下的选项，选项创建前会将该问题下的旧选项全部清空

        只有 checkbox、radio 两种问题才能使用本接口批量创建选项；

        Args:
            question_id(int): 问题 id；
            options(str): 选项数据，json 格式参数；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, question_id=question_id,
            options=json.dumps(options))
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/options/batch_create', data=data, timeout=timeout)

    def release_surveys(self, **kwargs):
        """根据参数筛选全部已发布问卷

        Args:
            survey_ids(str, 非必填): 问卷 id，逗号分割多个 id；
            developer_ids(str, 非必填): 开发者用户 id，逗号分割多个 id；
            release_survey_ids(str, 非必填): 已发布问卷 id，逗号分割多个 id；
            limesurvey_ids(str, 非必填): 底层问卷系统 limesurvey 的问卷 id，
                                        逗号分割多个 id；
            sort(str, 非必填): 以某字段排序，默认升序，字段前加上 “-” 代表降序；
            page(int, 非必填): 当前页，默认 1；
            limit(int, 非必填): 每页数量，默认 50
        Returns:
            Model: 问卷列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/release_surveys', data=data, timeout=timeout)
        return models.Model(result)

    def release_surveys_retrieve(self, release_survey_id):
        """根据编号获取已发布问卷

        Args:
            release_survey_id(int): 已发布问卷 id

        Returns:
            Model: 问卷数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            release_survey_id=release_survey_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/release_surveys/retrieve', data=data,
            timeout=timeout)
        return models.Model(result)

    def delete_release_surveys(self, release_survey_id):
        """根据问卷编号删除已发布问卷

        Args:
            release_survey_id(int): 已发布问卷 id；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            release_survey_id=release_survey_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post(
            '/api/survey/release_surveys/delete', data=data,
            timeout=timeout)

    def release_questions(self, release_survey_id, **kwargs):
        """根据参数筛选某已发布问卷中的问题

        Args:
            release_survey_id(int, 必填): 已发布问卷 id；
            release_question_ids(str, 非必填): 已发布问题 id，逗号分割多个 id；
            data_element_identifier_des(str, 非必填): 数据元编号，逗号分割多个；
            sort(str, 非必填): 以某字段排序，默认升序，字段前加上 “-” 代表降序；
            page(int, 非必填): 当前页，默认 1;
            limit(int, 非必填): 每页数量，默认 50;

        Returns:
            问题列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'release_survey_id': release_survey_id
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/release_questions', data=data, timeout=timeout)
        return models.Model(result)

    def release_questions_retrieve(self, release_question_id):
        """根据 id 获取已发布问题

        Args:
            release_question_id(int): 已发布问题 id；

        Returns:
            Model: 问题详情数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret,
            release_question_id=release_question_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/release_questions/retrieve', data=data,
            timeout=timeout)
        return models.Model(result)

    def survey_responses(self, **kwargs):
        """根据参数筛选回收到的答卷

        Args:
            response_ids(str, 非必填): 答卷 id，逗号分割多个 id；
            user_ids(str, 非必填): 用户系统 id，逗号分割多个 id；
            biosample_ids(str, 非必填): 生物样品编号，逗号分割多个；
            limeresponse_ids(str, 非必填): 底层问卷系统 limesurvey 中的答卷编号，
                                          逗号分割多个 id；
            release_survey_ids(str, 非必填): 已发布问卷 id，逗号分割多个；
            sort(str, 非必填): 以某字段排序，默认升序，字段前加上 “-” 代表降序；
            page(int, 非必填): 当前页，默认 1;
            limit(int, 非必填): 每页数量，默认 50;

        Returns:
            答卷列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/responses', data=data, timeout=timeout)
        return models.Model(result)

    def responses_retrieve(self, response_id):
        """根据编号获取答卷数据

        Args:
            response_id(int): 答卷 id；

        Returns:
            Model: 答卷数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, response_id=response_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/responses/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def import_response(self, user_id, biosample_id, release_survey_id,
                        answers):
        """将答卷导入到数据库中；

        Args:
            user_id(str): 用户系统 id；
            biosample_id(str): 生物样品编号；
            release_survey_id(int): 已发布问卷 id；
            answers(str): 答卷中的答案, json字符串；

        Returns:
            Model: 用户级问卷数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, user_id=user_id,
            biosample_id=biosample_id, release_survey_id=release_survey_id,
            answers=json.dumps(answers))
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/responses/import', data=data, timeout=timeout)
        return models.Model(result)

    def sync_responses(self, limesurvey_id, limeresponse_id, **kwargs):
        """将 limesurvey 中的答卷数据同步到问卷系统的答卷中

        limesurvey_id 和 limeresponse_id 相同时，重复调用本接口不会重复生成数据， 
        而是更新之前同步的那条数据；

        Args:
            limesurvey_id(int, 必填): 底层问卷 id；
            limeresponses_id(int, 必填): 底层答卷 id；
            user_id(int, 非必填): 答卷要绑定的用户 id；
            biosample_id(str, 非必填): 答卷要绑定的生物样品编号；

        Returns:
            Model: 用户与答卷数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'limesurvey_id': limesurvey_id,
            'limeresponse_id': limeresponse_id
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/responses/sync', data=data, timeout=timeout)
        return models.Model(result)

    def survey_answers(self, **kwargs):
        """根据参数筛选回收到的答案

        Args:
            response_ids(str, 非必填): 答卷 id，逗号分割多个 id；
            answer_ids(str, 非必填): 答案 id，逗号分割多个 id；
            user_ids(str, 非必填): 用户系统 id，逗号分割多个 id；
            biosample_ids(str, 非必填): 生物样品编号，逗号分割多个；
            concept_codes(str, 非必填): 标准数据定义关联代码（答案内容的关联代码），
                                       逗号分割多个；
            sort(str, 非必填): 以某字段排序，默认升序，字段前加上 “-” 代表降序；
            page(int, 非必填): 当前页，默认 1;
            limit(int, 非必填): 每页数量，默认 50;

        Returns:
            Model: 答案详情数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/answers', data=data, timeout=timeout)
        return models.Model(result)

    def latest_answers(self, user_id, data_element_identifier_des):
        """获取某个用户在某些问题上的最新提交的答案

        Args:
            user_id(str): 用户系统 id；
            data_element_identifier_des(str): 数据元编号，逗号分割多个；

        Returns:
            Model: 答案详情数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, user_id=user_id,
            data_element_identifier_des=data_element_identifier_des)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        ret = {}
        result = request.post(
            '/api/survey/answers/latest', data=data, timeout=timeout)
        ret['result'] = [models.Model(item) for item in result]
        return ret

    def answers_retrieve(self, answer_id):
        """根据答案编号获取答案

        Args:
            answer_id(int): 答案 id；

        Returns:
            Model: 答案详情数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, answer_id=answer_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/answers/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def survey_statistics(self, survey_id):
        """统计问卷将定时统计所有的问卷回收情况

        Args:
            survey_id(int): 问卷编号（未发布问卷的编号）;
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, survey_id=survey_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/statistics', data=data, timeout=timeout)
        return models.Model(result)

    def question_statistics(self, survey_id, data_element_identifier_de,
                            **kwargs):
        """分页获取问题相关答案的回收统计数据

        Args:
            survey_id(int): 问卷编号（未发布问卷的编号）;
            data_element_identifier_de(str): 问题绑定的数据元编号
            page(int, 非必填): 页码，大于等于 1；
            limit(int, 非必填): 单页返回数，最小值 1，最大值 100；

        Returns:
            问题统计数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'survey_id': survey_id,
            'data_element_identifier_de': data_element_identifier_de
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/statistics/question', data=data, timeout=timeout)
        return models.Model(result)

    def task_result(self, task_id):
        """根据任务编号获取异步任务运行结果

        Args:
            task_id(str): 任务 id；

        Returns:
            Model: 任务状态与返回结果
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, task_id=task_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/task', data=data, timeout=timeout)
        return models.Model(result)

    def survey_projects(self, project_ids):
        """获取项目绑定的已发布问卷

        Args:
            project_ids(str): 项目编号，逗号分割多个；

        Returns:
            项目编号与已发布问卷 id
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, project_ids=project_ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/projects', data=data, timeout=timeout)
        return models.Model(result)

    def survey_target(self, AND=None, OR=None, **kwargs):
        """从回收的答案中根据参数条件筛选定向推送的用户编号

        Args:
            AND(str, 非必填): “与逻辑”的筛选条件；
            OR(str, 非必填): 	“或逻辑”的筛选条件；
            page(int, 非必填): 当前页，默认 1;
            limit(int, 非必填): 每页数量，默认 50;

        Returns:
            用户列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'AND': json.dumps(AND),
            'OR': json.dumps(OR)
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/target', data=data, timeout=timeout)
        return models.Model(result)

    def question_size(self, user_id):
        """从回收的答案中统计用户已经回答过的问题数

        Args:
            user_id(str): 用户 id;

        Returns:
            用户已回答的问题数（按照 data_element_identifier_de 来统计）
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, user_id=user_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/api/survey/question_size', data=data, timeout=timeout)
        return models.Model(result)

    def wechat_profile(self, user_id):
        """通过 BGE 用户中心用户编号获取 BGE 主要小程序、公众号的 openid

        Args:
            user_id(str): 用户 id;

        Returns:
            Model: openid 相关数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, user_id=user_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/wechat/profile', data=data, timeout=timeout)
        return models.Model(result)

    def openbge_search(self, query, category, biosample_id=None, limit=50,
                       page=1):
        """搜索 BGE 的报告、变异位点、应用、研究所问卷

        Args:
            query(str): 搜索文本；
            category(str): 类别；
            biosample_id(str, 非必填): 生物样品编号；
            limit(int, 非必填): 单页数据返回数量，默认 50;
            page(int, 非必填): 单页数据返回数量，默认 1;

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, query=query, category=category,
            biosample_id=biosample_id, limit=limit, page=page)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/search', data=data, timeout=timeout)
        return models.Model(result)

    def create_index(self, type, content):
        """可以一次创建或更新多条索引

        Args:
            type(str): 索引类型，固定设置为 survey；
            content(list): 索引内容，json 格式的字符串；

        Returns:
            Model: 创建后的索引类
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, type=type,
            content=json.dumps(content))
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/index', data=data, timeout=timeout)
        ret = {}
        ret['result'] = [models.Model(item) for item in result]
        return ret

    def delete_index(self, type, ids):
        """一次删除多个索引

        Args:
            type(str): 索引类型，固定设置为 survey；
            ids(str): 要删除的问卷索引编号，多个编号以逗号分割，如：1,2,3；

        Returns:
            Model: 删除结果
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, type=type, ids=ids)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/index/delete', data=data, timeout=timeout)
        ret = {}
        ret['result'] = [models.Model(item) for item in result]
        return ret

    def gateway_invoke(self, service, api, **kwargs):
        """网关服务主要目的用于将无身份验证的其他项目接口通过本接口进行代理转发，
        对参数进行验证等，为接口提供签名认证的安全调用；

        Args:
            service(str): 服务名，请先在后台配置；
            api(str): 接口地址，根据后台配置的接口地址进行适配；
            params(str, 非必填): 需要转发的 GET 参数；
            headers(str, 非必填): 需要转发的 HTTP 头部；
            data(str, 非必填): 需要转发的 POST 数据；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'service': service,
            'api': api
        })
        data = make_sign(
            self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/gateway/invoke', data=data, timeout=timeout)
        return models.Model(result)

    def image_upload(self, image_path, allow_exif=False):
        """通过接口上传各种类型的图片，接口返回可访问的在线图片链接

        Args:
            image_path(str): 图片路径；
            allow_exif(bool, 非必填): 是否允许保存图片 exif 值；默认值：false；

        Returns:
            Model: 图片下载地址与md5值
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, allow_exif=allow_exif)
        files = {'image': image_path}
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose,
            content_type=None)
        result = request.post(
            '/service/image/upload', data=data, files=files,
            timeout=timeout)
        return models.Model(result)

    def sms(self, template, mobiles, **kwargs):
        """通用短信接口

        Args:
            template(str): 短信模板；
            mobiles(str): 手机号，逗号分割多个手机号，最多提供 100 个手机号；

        Kwargs:
            其他非必填参数参考接口文档
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        kwargs.update({
            'template': template,
            'mobiles': mobiles
        })
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        request.post('/service/sms', data=data, timeout=timeout)

    def sts_token(self):
        """获取阿里云第三方上传服务临时访问凭证

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/service/sts/token', data=data, timeout=timeout)
        return models.Model(result)

    def sign_url(self, object_name, region=None, expiration_time=None):
        """获取阿里云 OSS（对象存储）中的文件下载地址

        Args:
            object_name(str): OSS 对象;
            region(str): 区域，可选值：domestic、international；
            expiration_time(int): 下载地址过期时间;

        Returns:
            Model: 下载地址
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, object_name=object_name,
            region=region, expiration_time=expiration_time)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/service/oss/sign_url', data=data, timeout=timeout)
        return models.Model(result)

    def shorturls(self, url):
        """将长的网址转换为短网址

        Args:
            url(str): 要转为短网址的链接

        Returns:
            Model: 转换后的网址
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, url=url)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/service/shorturls', data=data, timeout=timeout)
        return models.Model(result)

    def bgicoin_withdraw(self, account_name, amount, order_type, order_id):
        """从华大员工华大币账户扣款付给商户

        Args:
            account_name(str): 付款的华大员工邮箱前缀；
            amount(str): 付款金额，必须大于 0；
            order_type(int): 订单类型，消费类型: 4线上消费，5体检，6线下消费;
            order_id(str): 第三方订单编号，需保证在第三方系统中唯一；订单号长度需大于或等于 8

        Returns:
            Model: 订单
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, account_name=account_name,
            amount=amount, order_type=order_type, order_id=order_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/service/bgicoin/withdraw', data=data, timeout=timeout)
        return models.Model(result)

    def wechat_token(self, app_id, action):
        """获取或更新微信公众号 access_token 的中控服务接口

        Args:
            app_id(str): BGE 微信公众号、小程序的 app_id;
            action(str): 可选项 get、refresh；

        Returns:
            Model: token
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, app_id=app_id, action=action)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/wechat/token', data=data, timeout=timeout)
        return models.Model(result)

    def invoke_task(self, task_name, invocation_type='async', args=None,
                    kwargs=None):
        """调用任务

        Args:
            task_name(str): 任务名称；
            invocation_type(str): 任务类型，可选项 sync、async
        Returns:
            任务名称
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        args = json.dumps(args or [])
        kwargs = json.dumps(kwargs or [])
        data = make_sign(
            self.app_key, self.app_secret, task_name=task_name,
            invocation_type=invocation_type, args=args, kwargs=kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/task/invoke', data=data, timeout=timeout)
        return models.Model(result)

    def model_list(self, **kwargs):
        """模型列表

        Args:
            model_ids(str, 非必填): 模型id；
            page(int, 非必填): 页码；
            limit(int, 非必填): 每页数量

        Returns:
            模型列表
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model', data=data, timeout=timeout)
        return models.Model(result)

    def deploy_model(self, model_id, object_name=None, runtime=None,
                     handler=None, memory_size=None, model_timeout=None):
        """部署模型

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, model_id=model_id,
            object_name=object_name, runtime=runtime, handler=handler,
            memory_size=memory_size, timeout=model_timeout)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model/deploy', data=data, timeout=timeout)
        return models.Model(result)

    def publish_model(self, model_id, message):
        """发布模型

        Args:
            model_id(str): 模型 id;
            message(str): 备注信息；

        Returns:
            Model: 任务id

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, model_id=model_id,
                         message=message)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model/publish', data=data, timeout=timeout)
        return models.Model(result)

    def rollback_model(self, model_id, version):
        """回滚模型

        Args:
            model_id(str): 模型 id;
            version(int): 模型版本；

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, model_id=model_id,
                         version=version)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model/rollback', data=data, timeout=timeout)
        return models.Model(result)

    def retrieve_model(self, model_id):
        """模型详情数据

        Args:
            model_id(str): 模型 id；

        Returns:
            模型数据
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, model_id=model_id)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def model(self, model_id, draft=False, **kwargs):
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        url = '/openbge/model/%s' % model_id
        if draft:
            url = '/openbge/model/%s/draft' % model_id
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(url, data=data, timeout=timeout)
        if isinstance(result, list):
            # 新版本模型返回的 data 都是 dict 类型
            # 但上古模型 B7tsXHBhkFs816j 和 JETGJz5ncmMlVUK 返回值为 list，需特殊处理；
            ret = []
            for item in result:
                ret.append(models.Model(item))
            return ret
        else:
            return models.Model(result)

    def model_versions(self, model_id, **kwargs):
        """获取模型版本

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        url = '/openbge/model/{}/versions'.format(model_id)
        result = request.post(url, data=data, timeout=timeout)
        return models.Model(result)

    def model_doc_upload(self, doc_tab, model_id, doc_content):
        """上传模型文档

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, doc_tab=doc_tab,
            model_id=model_id, doc_content=doc_content)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model/doc_upload', data=data, timeout=timeout)
        return models.Model(result)

    def upload_model_expfs(self, model_id, expfs):

        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, model_id=model_id)
        files = {'expfs': open(str(expfs), 'rb')}
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/model/doc_upload', data=data, files=files,
            timeout=timeout)
        return models.Model(result)

    def watch_fc2(self, trigger, event):

        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, trigger=trigger,
                         event=event)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/watch/fc2', data=data, timeout=timeout)
        return models.Model(result)

    def get_sample_V2(self, **kwargs):
        """新版获取样本数据

        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret, **kwargs)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/v2/openbge/samples', data=data, timeout=timeout)
        return models.Model(result)

    def task(self, task_id):
        """获取任务结果

        Args:
            task_id(str): 任务 id

        Returns:
            models: 任务结果
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(self.app_key, self.app_secret)
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/openbge/task/{}'.format(task_id), data=data, timeout=timeout)
        return models.Model(result)

    def openplatform_samples_state(self, biosample_id, sub_state, mtime,
                                   change_source=None, comment=None):
        """更改样品状态

        Args:
            biosample_id(str, 必填): 样品编号；
            sub_state(int, 必填): 样品子状态；
            change_source(str, 非必填): 样品状态更新来源；
            mtime(非必填): 样品更新时间；
            comment(json, 非必填): 样品状态备注信息 json 格式；
        """
        comment = comment if comment else None
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key, self.app_secret, biosample_id=biosample_id,
            sub_state=sub_state, change_source=change_source, mtime=mtime,
            comment=comment
        )
        request = HTTPRequest(
            self.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            'openbge/openplatform/samples/state', data=data,
            timeout=timeout)
        return result

    def invoke_notify(self, notify_generator, category, sub_category=None,
                      params=None):
        """发送通知

        Args:
            notify_generator(str, 必填): 通知生成点；
            category(str, 必填): 消息渠道；
            sub_category(str, 非必填): 子消息渠道；
            params(json, 非必填): 通知内容的相关参数
        """
        params = json.dumps(params) if params else None
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries

        data = make_sign(
            self.app_key,
            self.app_secret,
            notify_generator=notify_generator,
            category=category,
            sub_category=sub_category,
            params=params
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            'notify_center/invoke/notify',
            data=data,
            timeout=timeout
        )
        return result

    def ferry_download_to_oss(self, account, password, project_no,
                              biosample_cnt, included_filename_exts=None,
                              sample_names=None, action=None):
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            account=account,
            password=password,
            project_no=project_no,
            biosample_cnt=biosample_cnt,
            included_filename_exts=included_filename_exts,
            sample_names=sample_names,
            action=action
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            '/service/ferry/download_to_oss',
            data=data,
            timeout=timeout
        )
        return models.Model(result)

    def add_sms_template(self, api_name, sign_name, template_type,
                         template_name, template_content, remark):
        """申请短信模板

        Args:
            api_name(str, 必填): 接口名；
            sign_name(str, 必填): 短信签名名称；
            template_type(int, 必填): 短信类型；
            template_name(str, 必填): 模板名称；
            template_content(str, 必填): 模板内容；
            remark(str, 必填): 场景说明
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            api_name=api_name,
            sign_name=sign_name,
            template_type=template_type,
            template_name=template_name,
            template_content=template_content,
            remark=remark
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            'service/sms/add_template',
            data=data,
            timeout=timeout
        )
        return models.Model(result)

    def modify_sms_template(self, template_code, template_type,
                            template_name, template_content, remark):
        """需改未审核通过的短信模板

        Args:
            template_code(str, 必填): 短信模板code；
            template_type(int, 必填): 短信类型；
            template_name(str, 必填): 模板名称；
            template_content(str, 必填): 模板内容；
            remark(str, 必填): 场景说明
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            template_code=template_code,
            template_type=template_type,
            template_name=template_name,
            template_content=template_content,
            remark=remark
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            'service/sms/modify_template',
            data=data,
            timeout=timeout
        )
        return models.Model(result)

    def delate_sms_template(self, template_code, api_name):
        """删除短信模板

        Args:
            template_code(str, 必填): 短信模板code；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            template_code=template_code,
            api_name=api_name
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            'service/sms/delete_template',
            data=data,
            timeout=timeout
        )
        return models.Model(result)

    def template_status(self, template_codes):
        """更新模板状态

        Args:
            template_codes(str, 必填): 短信模板code；
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            template_codes=template_codes
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            'service/sms/template_status',
            data=data,
            timeout=timeout
        )
        return models.Model(result)

    def update_msgs_status(self, msg_ids):
        """更新批量发送短信状态及统计

        Args:
            batch_ids(str, 必填): 批量发送 ids
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            msg_ids=msg_ids
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose,
        )
        result = request.post(
            'service/sms/update_msgs_status',
            data=data,
            timeout=timeout
        )
        return models.Model(result)

    def batch_send_sms(self, template_api_name, title, mobiles,
                       template_params):
        """批量发送短信

        Args:
            template_api_name(str, 必填)：短信模板api_name
            title(str, 必填): 批量发送标题
            mobiles(str, 必填): 手机号，多个手机号用 , 隔开
            template_params(list, 必填): 模板参数，个数应与手机号数量相同
        """
        timeout = self.timeout
        verbose = self.verbose
        max_retries = self.max_retries
        data = make_sign(
            self.app_key,
            self.app_secret,
            template_api_name=template_api_name,
            title=title,
            mobiles=mobiles,
            template_params=json.dumps(template_params)
        )
        request = HTTPRequest(
            self.endpoint,
            max_retries=max_retries,
            verbose=verbose
        )
        result = request.post(
            'service/sms/batch_send',
            data=data,
            timeout=timeout
        )
        return models.Model(result)


class Account(object):
    def __init__(self, inst):
        self.inst_ref = ref(inst)

    def verify(self, account, scope, user_id=None):
        """发送验证码

        发送短信、邮件验证码；验证码可用于登录、注册、更新手机号、更新邮箱地址；

        Args:
            account (str): 接收验证码的手机号或者邮箱；
            scope (str): 使用验证码的场景，可选值：login（登录）, register（注册）, 
                         update（更新手机号或者邮件地址）；
            user_id (str, optional): 要更新邮箱或手机号的用户编号，仅 scope=update 时
                                     必须提供，其他 scope 无需提供；
        """
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            account=account,
            scope=scope,
            user_id=user_id
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/account/verify', data=data, timeout=timeout)
        return models.Model(result)

    def login(self, account, password=None, code=None):
        """用户可使用手机、邮箱通过验证码或密码完成登录验证

        Args:
            account (str): 用于注册和接收到验证码的手机号或者邮箱
            password (str, optional): 密码，password 与 code 必须且只能提供其中之一
            code (str, optional): 短信或邮件中收到的6个数字的验证码，password 与 code 
                                  必须且只能提供其中之一；
        """
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            account=account,
            password=password,
            code=code
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/account/login', data=data, timeout=timeout)
        return models.Model(result)

    def get_users(self, user_ids=None, page=1, limit=100, sort=None):
        """查询用户列表

        根据查询条件查询 BGE 用户中心的用户

        Args:
            user_ids (str, optional): 用户编号；逗号分割多个；
            page (int, optional): 页码；默认值为 1；
            limit (int, optional): 单页返回数量；默认值为 100；
            sort (str, optional): 排序，逗号分割多个；可选排序字段：user_id、gender、
                                  date_joined、last_login、last_modified；字段前
                                  增加减号代表从大到小排序；无减号代表从小到大；
                                  示例：last_login,-gender；
        """
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            user_ids=user_ids,
            page=page,
            limit=limit,
            sort=sort
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/account/users', data=data, timeout=timeout)
        return models.Model(result)

    def get_user(self, user_id=None, token=None):
        """获取用户信息

        通过 user_id 或者登录返回的 token 获取用户详细信息；

        Args:
            user_id (str, optional): 用户编号；与 token 同一时间只允许提供其中之一；
            token (str, optional): 登录验证成功后返回的 token；
        """
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            token=token,
            user_id=user_id
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/account/user', data=data, timeout=timeout)
        return models.Model(result)


class Report(object):
    def __init__(self, inst):
        self.inst_ref = ref(inst)

    def retrieve(self, report_id):
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            report_id=report_id
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/report/retrieve', data=data, timeout=timeout)
        return models.Model(result)

    def start_qc(self, report_id):
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            report_id=report_id
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/report/start_qc', data=data, timeout=timeout)
        return models.Model(result)

    def check_qc(self, report_id):
        inst = self.inst_ref()
        timeout = inst.timeout
        verbose = inst.verbose
        max_retries = inst.max_retries
        data = make_sign(
            inst.app_key,
            inst.app_secret,
            report_id=report_id
        )
        request = HTTPRequest(
            inst.endpoint, max_retries=max_retries, verbose=verbose)
        result = request.post(
            '/report/check_qc', data=data, timeout=timeout)
        return models.Model(result)