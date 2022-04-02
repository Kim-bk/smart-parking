package com.parkingsmart.service;

import java.util.List;

import com.parkingsmart.dto.ProvinceDTO;

public interface IProvinceService {
	public List<ProvinceDTO> findAll();
	public ProvinceDTO findOneById(String id);

}
