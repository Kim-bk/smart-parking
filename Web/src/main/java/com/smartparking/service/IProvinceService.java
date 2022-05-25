package com.smartparking.service;

import java.util.List;

import com.smartparking.dto.ProvinceDTO;

public interface IProvinceService {
	
	public List<ProvinceDTO> findAll();
	public ProvinceDTO findOneById(String id);


}
