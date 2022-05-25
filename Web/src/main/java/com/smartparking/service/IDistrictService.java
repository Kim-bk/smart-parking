package com.smartparking.service;

import java.util.List;

import com.smartparking.dto.DistrictDTO;


public interface IDistrictService {
	
	
	public List<DistrictDTO> findByIdProvince(String id);
	public DistrictDTO findById(String id);

}
