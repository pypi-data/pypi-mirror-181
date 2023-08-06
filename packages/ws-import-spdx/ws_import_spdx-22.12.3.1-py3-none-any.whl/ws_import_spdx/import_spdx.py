import argparse
import csv
import datetime
import json
import logging
import os
import sys
import http.client
import re
import hashlib
from ws_sdk import web

from ws_import_spdx._version import __version__, __tool_name__
from ws_import_spdx.import_const import SHA1CalcType

logger = logging.getLogger(__tool_name__)
logger.setLevel(logging.DEBUG)
is_debug = logging.DEBUG if bool(os.environ.get("DEBUG", 0)) else logging.INFO

formatter = logging.Formatter('%(levelname)s %(asctime)s %(thread)d %(name)s: %(message)s')
s_handler = logging.StreamHandler()
s_handler.setFormatter(formatter)
s_handler.setLevel(is_debug)
logger.addHandler(s_handler)
logger.propagate = False


def parse_args():
    parser = argparse.ArgumentParser(description='Utility to load SBOM report to Mend')
    parser.add_argument('-u', '--userKey', help="WS User Key", dest='ws_user_key',
                        default=os.environ.get("WS_USER_KEY"),
                        required=True if not os.environ.get("WS_USER_KEY") else False)
    parser.add_argument('-k', '--token', help="WS Key", dest='ws_token', default=os.environ.get("WS_TOKEN"),
                        required=True if not os.environ.get("WS_TOKEN") else False)
    parser.add_argument('-s', '--scope', help="Project token for updating ", dest='scope_token',
                        default=os.environ.get("WS_SCOPE_TOKEN"))
    parser.add_argument('-p', '--project', help="WS PROJECT NAME", dest='ws_project',
                        default=os.environ.get("WS_PROJECT_NAME", ''))
    parser.add_argument('-pr', '--product', help="WS PRODUCT Token", dest='ws_product', required=True,
                        default=os.environ.get("WS_PRODUCT_TOKEN", ''))
    parser.add_argument('-sbom', '--sbom', help="SBOM Report for upload", dest='sbom', required=True,
                        default=os.environ.get("SBOM", ''))
    parser.add_argument('-t', '--updatetype', help="Update type", dest='update_type',
                        default=os.environ.get("UPDATE_TYPE", 'OVERRIDE'))
    parser.add_argument('-o', '--out', help="Output directory", dest='out_dir', default=os.getcwd())
    parser.add_argument('-a', '--wsUrl', help="WS URL", dest='ws_url',
                        default=os.environ.get("WS_URL", 'saas.whitesourcesoftware.com'))
    parser.add_argument('-l', '--load', help="Load to Mend", dest='load', default='true')
    arguments = parser.parse_args()

    return arguments


def check_el_inlist(name: str) -> bool:
    res = False
    for rel in relations:
        for key, value in rel.items():
            if 'SPDXRef-PACKAGE-' + name == value:
                res = True
                break
    return res


def get_element_by_spdxid(spdx: str) -> dict:
    out_el = {}
    for el in pkgs:
        if el["SPDXID"] == spdx:
            try:
                sha1 = f"{el['checksums'][0]['checksumValue']}"
            except:
                sha1 = ''
            try:
                chld = el['children']
            except:
                chld = []
            try:
                out_el = {
                    "artifactId": f"{el['packageFileName']}",
                    "version": f"{el['versionInfo']}",
                    "sha1": sha1,
                    "systemPath": "",
                    "optional": False,
                    "filename": f"{el['packageFileName']}",
                    "checksums": {
                        "SHA1": sha1
                    },
                    "dependencyFile": "",
                    "children": chld
                }
            except:
                pass
            break
    return out_el


def add_child(element: dict) -> dict:  # recursion for adding children
    new_el = element
    name = element['artifactId']
    for rel in relations:
        for key, value in rel.items():
            if key == 'SPDXRef-PACKAGE-' + name:
                chld_el = get_element_by_spdxid(value)
                try:
                    new_el['children'].append(chld_el)
                except:
                    new_el['children'] = [chld_el]
                added_el.append(chld_el['artifactId'])
                add_child(chld_el)
    return new_el


def csv_to_json(csv_file):
    data = {}
    dep = []

    # Open a csv reader called DictReader
    count = 0
    try:
        with open(csv_file, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)

            # Convert each row into a dictionary
            # and add it to data
            for rows in csvReader:
                key = count
                data[key] = rows
                count +=1
        csvf.close()

        json_ = json.loads(json.dumps(data, indent=4))
        for el_ in json_:
            pck = {
                "name" : json_[el_]["name"],
                "licenseConcluded" : json_[el_]["licenseConcluded"],
                "licenseInfoFromFiles" : json_[el_]["licenseInfoFromFiles"],
                "licenseDeclared" : json_[el_]["licenseDeclared"],
                "copyrightText" : json_[el_]["copyrightText"],
                "versionInfo" : json_[el_]["versionInfo"],
                "packageFileName" : json_[el_]["packageFileName"],
                "supplier" : json_[el_]["supplier"],
                "originator" : json_[el_]["originator"],
                "homepage" : json_[el_]["homepage"],
                "filesAnalyzed" : False,
                "checksums" : [{"algorithm": "SHA1", "checksumValue": json_[el_]["sha1"]}]
            }
            dep.append(pck)
    except:
        pass

    return dep


def create_body(args):
    def create_add_sha1(langtype = ""): # maybe we will need to calculate additional sha1 later
        try:
            for ext_ref in package['externalRefs']:
                if ext_ref['referenceCategory'] == "PACKAGE_MANAGER":
                    pkgname = re.search(r"pkg:(.*?)/", ext_ref['referenceLocator'], flags=re.DOTALL).group(1).strip()
                    lang_type = SHA1CalcType.get_package_type(f_t=pkgname)
                    if lang_type.lower_case == "y":
                        str = f"{package['name'].lower()}_{package['versionInfo'].lower()}_{lang_type.language}"
                    else:
                        str = f"{package['name']}_{package['versionInfo']}_{lang_type.language}"
                    break
        except Exception as err:
            if langtype == "":
                return ""
            else:
                if SHA1CalcType.get_package_data(lng=langtype) == "y":
                    str = f"{package['name'].lower()}_{package['versionInfo'].lower()}_{langtype}"
                else:
                    str = f"{package['name']}_{package['versionInfo']}_{langtype}"
        return hashlib.sha1(str.encode("utf-8")).hexdigest()

    def get_pkg_parent(pkg_child : str):  # if will be needed to upload source files
        res = ""
        try:
            rels = sbom["relationships"]
            for rel_ in rels:
                if rel_["relationshipType"] == "DYNAMIC_LINK" and rel_["relatedSpdxElement"] == pkg_child:
                    res = rel["spdxElementId"]
                    break
        except:
            pass
        return res

    def search_lib_by_name(lib_name, lib_ver, lib_type):
        sha1 = lname = ""
        try:
            lib_lst = web.WS.call_ws_api(self=args.ws_conn, request_type="getBasicLibraryInfo",
                                             kv_dict={"libraryName": lib_name, "libraryVersion": lib_ver,
                                                      "libraryType": lib_type})
            for lib_ in lib_lst['librariesInformation']:
                try:
                    sha1 = lib_['sha1']
                except:
                    pass
                try:
                    lname = lib_['artifactId']
                except:
                    pass
                break
        except:
            pass
        return sha1, lname

    ts = round(datetime.datetime.now().timestamp())
    global relations
    global pkgs
    global added_el
    global sbom
    relations = []
    added_el = []
    dep = []

    try:
        if os.path.splitext(args.sbom)[1] == ".json":
            f = open(args.sbom, "r",encoding="utf-8")
            sbom = json.load(f)
        elif os.path.splitext(args.sbom)[1] == ".csv":
            sbom = csv_to_json(args.sbom)
        else:
            logger.error(f"Error opening SBOM file: {args.sbom}. The format is not supported")
            exit(-1)
    except Exception as err:
        logger.error(f"Error opening SBOM file: {err}")
        exit(-1)

    try:
        for rel in sbom["relationships"]:
            if rel['relationshipType'] == "DEPENDS_ON":
                relations.append({rel['spdxElementId']: rel['relatedSpdxElement']})
    except:
        pass

    try:
        pkgs = sbom["packages"] # from JSON
    except:
        pkgs = sbom  # from CSV

    for package in pkgs:
        try:
            sha1 = f"{package['checksums'][0]['checksumValue']}"
        except:
            sha1 = ''

        try:
            pkg_name = package["packageFileName"]
        except:
            pkg_name = package["name"]

        if sha1 != '':
            pck = {
                "artifactId": f"{pkg_name}",
                "version": f"{package['versionInfo']}",
                "sha1": sha1,
                "systemPath": "",
                "optional": False,
                "filename": f"{pkg_name}",
                "checksums": {
                    "SHA1": sha1
                },
                "dependencyFile": ""
            }
        else:     # SHA1 not found
            pck = {}
            lang_types = []
            try:
                pck_ext = package["externalRefs"]   # execute SPDX structure file
                # like cpe:2.3:a:python:botocore:1.22.12:*:*:*:*:*:*:*
                for ext_ref in pck_ext:
                    if ext_ref["referenceCategory"] == "PACKAGE_MANAGER" or ext_ref[
                        'referenceCategory'] == "PACKAGE-MANAGER":
                        pkgname = re.search(r"pkg:(.*?)/", ext_ref['referenceLocator'], flags=re.DOTALL).group(
                            1).strip()
                        pkg_data = SHA1CalcType.get_package_type(f_t=pkgname)
                        if pkg_data:
                            lang_types.append({pkg_data.libtype : pkg_data.ext})
                            break
            except:
                try:
                    if pkg_name != "NOASSERTION":
                        ext_name = os.path.splitext(pkg_name)[1][1:]
                        logger.info(f"Looking for package {pkg_name} in Mend")
                        if ext_name == "":  # type of extension was not provided. Taken all possible types
                            for calctype_ in SHA1CalcType:
                                lang_types.append({calctype_.libtype : calctype_.ext})
                        else:
                            type_lst = SHA1CalcType.get_package_type_list_by_ext(ext=ext_name)
                            if type_lst == []:
                                for calctype_ in SHA1CalcType:  # the extension was defined not correct
                                    # (it could be part of package name)
                                    lang_types.append({calctype_.libtype: calctype_.ext})
                            else:
                                for type_lst_ in type_lst:
                                    lang_types.append({type_lst_.libtype : type_lst_.ext})
                except:
                    pass

            sha1_ = ""
            for l_type in lang_types:
                for key, value in l_type.items():
                    sha1_, lname_ = search_lib_by_name(lib_name=pkg_name, lib_ver=package['versionInfo'], lib_type=key)
                if sha1_ != "":
                    pck = {
                        "artifactId": f"{lname_}",
                        "version": f"{package['versionInfo']}",
                        "sha1": sha1_,
                        "systemPath": "",
                        "optional": False,
                        "filename": f"{lname_}-{package['versionInfo']}.{value}",
                        "checksums": {
                            "SHA1": sha1_
                        },
                        "dependencyFile": ""
                    }
                    break
            if sha1_ == "" and pkg_name != "NOASSERTION":
                logger.info(f"The package {pkg_name} was not found in Mend (not enough data for localization)")

        if not check_el_inlist(pkg_name) and pck != {}:
            if pkg_name not in added_el:
                added_el.append(f"{pkg_name}")  # we add element to list if was not added before
                dep.append(add_child(pck))
            '''   
            if sha1_ == "":
                for l_type in lang_types:
                    for key, value in l_type.items():
                        add_sha1 = create_add_sha1(key)

                    if add_sha1 != "":
                        pck = {
                            "artifactId": f"{lname_ if lname_ != '' else pkg_name}",
                            "version": f"{package['versionInfo']}",
                            "systemPath": "",
                            "optional": False,
                            "filename": f"{lname_ if lname_ != '' else pkg_name}-{package['versionInfo']}.{value}",
                            "additionalSha1": f"{add_sha1}",
                            "dependencyFile": "",
                            "dependencyType": "NOASSERTION"
                        }
                        if not check_el_inlist(pkg_name) and pck != {}:
                            if pkg_name not in added_el:
                                added_el.append(f"{pkg_name}")  # we add element to list if was not added before
                                dep.append(add_child(pck))
            else:
                if not check_el_inlist(pkg_name) and pck != {}:
                    if pkg_name not in added_el:
                        added_el.append(f"{pkg_name}")  # we add element to list if was not added before
                        dep.append(add_child(pck))
            '''
    if args.scope_token == '' or args.scope_token is None:
        prj = [
            {
                "coordinates": {
                    "artifactId": f"{args.ws_project}"
                },
                "dependencies": dep
            }
        ]
    else:
        prj = [
            {
                "dependencies": dep,
                "projectToken": f"{args.scope_token}"
            }
        ]

    out = {
        "updateType": f"{args.update_type}",
        "type": "UPDATE",
        "agent": "fs-agent",
        "agentVersion": "",
        "pluginVersion": "",
        "orgToken": f"{args.ws_token}",
        "userKey": f"{args.ws_user_key}",
        "product": f"{args.ws_product}",
        "productVersion": "",
        "timeStamp": ts,
        "projects": prj
    }
    return out


def json_to_csv_(json_file_name, csv_file_name):
    with open(json_file_name, "r") as json_file:
        data = json.load(json_file)
    data_file = open(csv_file_name, 'w', encoding="utf-8", newline='')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0
    entity = data['packages']

    for ent_ in entity:
        if count == 0:
            # Writing headers of CSV file
            header = ent_.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        new_ent = {}
        for key,value in ent_.items():
            if type(ent_[key]) is str:
                new_ent[key] = value
            elif type(ent_[key]) is list:
                if type(ent_[key][0]) is dict:
                    new_ent[key] = value[0]['checksumValue']
                else:
                    new_ent[key] = value[0]
            else:
                new_ent[key] = ""

        csv_writer.writerow(new_ent.values())

    data_file.close()


def get_files_from_pck(pck, sbom_f):
    file_lst = []
    try:
        f = pck['hasFiles']
        files = [*set(f)]
    except:
        files = []
    for file_ in files:
        file_lst.append(get_file_by_spdx(file_,sbom_f))
    return file_lst


def get_file_by_spdx(spdx, sbom_f):
    file_data = {}
    for d in sbom_f:
        if d['SPDXID'] == spdx:
            sbom_f_ = d
            break

    if sbom_f_:
        try:
            sha1 = f"{sbom_f_['checksums'][0]['checksumValue']}"
        except:
            sha1 = ""
        try:
            vers = f"{sbom_f_['versionInfo']}"
        except:
            vers = ""
        try:
            file_data = {
                "artifactId": f"{spdx}",
                "version": vers,
                "sha1": sha1,
                "systemPath": "",
                "optional": False,
                "filename": f"{sbom_f_['fileName']}",
                "checksums": {
                    "SHA1": sha1
                },
                "dependencyFile": f"{sbom_f_['fileName']}"
            }
        except:
            pass
    return file_data


def upload_to_mend(upload):
    ts = round(datetime.datetime.now().timestamp())
    ret = False
    try:
        conn = http.client.HTTPSConnection(f"{args.ws_url}")
        json_prj = json.dumps(upload['projects'])  # API understands just JSON Array type, not simple List

        payload = f"type=UPDATE&updateType={args.update_type}&agent=fs-agent&agentVersion=1.0&token={args.ws_token}&" \
                  f"userKey={args.ws_user_key}&product={args.ws_product}&timeStamp={ts}&diff={json_prj}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn.request("POST", "/agent", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())
        if data['status'] == 1:
            ret = True
            logger.info("Data was updated/created successfully")
        else:
            logger.error(f"Impossible to load. {data['message']} ({data['data']})")
        conn.close()
    except Exception as err:
        logger.error(f"Error during upload data to Mend: {err}")
    return ret


def main():
    global output_json
    global args
    output_json = {}
    try:
        args = parse_args()
        logger.info("Started creation upload request")
        args.ws_conn = web.WSApp(url=f"https://{args.ws_url}",
                                 user_key=args.ws_user_key,
                                 token=args.ws_token,
                                 tool_details=(f"ps-{__tool_name__.replace('_', '-')}", __version__))
        if not os.path.exists(args.out_dir):
            logger.info(f"Dir: {args.out_dir} does not exist. Creating it")
            os.mkdir(args.out_dir)
        full_path = os.path.join(args.out_dir, f"Mend_upload_{datetime.datetime.now().strftime('%Y%m%d')}.json")

        if (args.scope_token == '' or args.scope_token is None) and (args.ws_project == '' or args.ws_project is None):
            logger.error("Project name or project token have to be defined")
            exit(-1)

        output_json = create_body(args)
        if args.load.lower() == "true":
            logger.info("Uploading data to Mend")
            if upload_to_mend(output_json):
                logger.info("Upload data finished successfully")

        with open(full_path, 'w') as outfile:
            json.dump(output_json, outfile, indent=4)
        logger.info(f"Upload request created successfully [{full_path}]")
    except Exception as err:
        logger.error(f"Error creating upload file: {err}")


if __name__ == '__main__':
    sys.exit(main())
